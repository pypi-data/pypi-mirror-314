import functools
import io
import json
import lzma
import math
import pickle
import yaml
import re
import zlib
from pathlib import Path
from types import ModuleType
from typing import Any, Callable, Literal, Union
import operator
from psplpy.other_utils import get_key_from_value


class _ComparisonMeta(type):
    def __new__(cls, name, bases, dct):
        # Using this way can avoid the function in loop using the last iteration's value
        # or using a default kwarg, but that would create an unnecessary kwarg
        def create_func(op):
            def method(self, other):
                if isinstance(other, self.__class__):
                    return getattr(operator, op)(self.bit_value, other.bit_value)
                elif isinstance(other, int):
                    return getattr(operator, op)(self.bit_value, other)
                elif isinstance(other, bytes):
                    return getattr(operator, op)(self.bit_value, int.from_bytes(other, byteorder='big'))
                return NotImplemented   # __eq__ and __ne__ will return True or False, can't reach there
            return method

        for op in ['lt', 'le', 'gt', 'ge', 'eq', 'ne']:
            dct[f'__{op}__'] = create_func(op)
        return super().__new__(cls, name, bases, dct)


class BitManipulator(metaclass=_ComparisonMeta):
    _EXCEED_BITS_ERR_INFO = "Bit value's length must be less than or equal to {}"

    def __init__(self, bit_value: Union[int, bytes, 'BitManipulator'] = 0,
                 max_bits: int = None, fixed_bits: int = None):
        self.max_bits = max_bits
        self.fixed_bits = fixed_bits
        if isinstance(bit_value, bytes):
            bit_value = int.from_bytes(bit_value, byteorder='big')
        if isinstance(bit_value, BitManipulator):
            bit_value = bit_value.bit_value
        if isinstance(bit_value, int):
            if bit_value < 0:
                raise ValueError("Bit value must be a non-negative integer")
            self._set_bit_value(bit_value)
        else:
            raise ValueError("Bit value must be an int or bytes object")

    def _check_bits(self, length: int) -> None:
        if self.max_bits is not None and length > self.max_bits:
            raise ValueError(self._EXCEED_BITS_ERR_INFO.format('max_bits'))
        if self.fixed_bits is not None and length > self.fixed_bits:
            raise ValueError(self._EXCEED_BITS_ERR_INFO.format('fixed_bits'))

    def _set_bit_value(self, bit_value: int) -> None:
        self._check_bits(bit_value.bit_length())
        self.bit_value = bit_value

    def __len__(self):
        return self.bit_value.bit_length()

    def _index_check(self, index: int) -> int:
        if index < 0:
            index += len(self)
            if index < 0:
                raise IndexError("Index out of range")
        return index

    def _get_iter_range(self, key: slice) -> list:
        return list(range(*key.indices(key.stop if key.stop > 0 else len(self))))

    def __getitem__(self, key: int | slice) -> str:
        if isinstance(key, slice):
            return ''.join([self[i] for i in self._get_iter_range(key)])
        elif isinstance(key, int):
            return str((self.bit_value >> self._index_check(key)) & 1)
        raise TypeError("Invalid argument type")

    def __setitem__(self, key: int | slice, value: int | str) -> None:
        def _set_bit(index: int, bit: int) -> None:
            if bit == 1:
                self._set_bit_value(self.bit_value | (1 << index))  # Set bit to 1
            elif bit == 0:
                self._set_bit_value(self.bit_value & ~(1 << index))  # Set bit to 0
            else:
                raise ValueError("Value must be 0 or 1")

        if isinstance(key, slice):
            iter_range = self._get_iter_range(key)
            if isinstance(value, int):
                value = bin(value)[2:]
            if len(value) != len(iter_range):
                raise ValueError(f"Slice length {len(iter_range)} not equal to the value length {len(value)}")
            original_bit_value = self.bit_value
            try:
                for i, bit_index in enumerate(iter_range):
                    _set_bit(bit_index, int(value[i]))
            except ValueError as e:
                self._set_bit_value(original_bit_value)
                raise e
        elif isinstance(key, int):
            _set_bit(self._index_check(key), int(value))
        else:
            raise TypeError("Invalid argument type")

    def get_bit(self, key: int | slice) -> str:
        return self[key]

    def set_bit(self, key: int | slice, value: int | str | bytes) -> None:
        self[key] = value

    def to_bytes(self, length: int = None) -> bytes:
        """Convert the bit value to bytes. The length specifies the number of bytes."""
        if length is None:
            bit_length = len(self)
            if self.fixed_bits is not None:
                bit_length = self.fixed_bits
            length = math.ceil(bit_length / 8)
        return self.bit_value.to_bytes(length, byteorder='big')

    def __format__(self, format_spec: Literal["b", "o", "x", "d"]):
        """Support custom formatting: 'b' for binary, 'o' for octal, 'x' for hex, 'd' for decimal."""
        if format_spec in ["b", "o", "x", "d"]:
            if self.fixed_bits and format_spec == "b":
                return f'{self.bit_value:{format_spec}}'.zfill(self.fixed_bits)
            return f'{self.bit_value:{format_spec}}'
        return str(self)

    def __str__(self):
        # Return the bit value as a binary string, MSB first
        return self.__format__('b')

    __repr__ = __str__

    def __iter__(self):
        for position in range(len(self)):
            yield self[position]


class Compressor:
    LZMA = 'lzma'
    ZLIB = 'zlib'

    def __init__(self, lib: str = ZLIB):
        self.lib = lib

    def compress(self, data: bytes, lib: str = '') -> bytes:
        lib = lib or self.lib
        compressed_data = globals()[lib].compress(data)
        return compressed_data

    def decompress(self, compressed_data: bytes, lib: str = '') -> bytes:
        lib = lib or self.lib
        data = globals()[lib].decompress(compressed_data)
        return data


def _check_int_or_float(input_str: str) -> type:
    int_pattern = r'^[-+]?\d+$'
    float_pattern = r'^[-+]?\d+(\.\d+)?$'

    if re.match(int_pattern, input_str):
        return int
    elif re.match(float_pattern, input_str):
        return float
    else:
        return str


def _convert_json_dict_key_to_number(data: Any) -> Any:
    if isinstance(data, dict):
        # if data type is dict, convert it
        converted_dict = {}
        for key, value in data.items():
            if type(key) == str:
                trans_type = _check_int_or_float(key)
                key = trans_type(key)
            # process the values in dict, using recursion
            value = _convert_json_dict_key_to_number(value)
            converted_dict[key] = value
        return converted_dict
    elif isinstance(data, (list, tuple, set)):
        # if date type is list, tuple or set, process it recursively
        converted_list = []
        for item in data:
            converted_item = _convert_json_dict_key_to_number(item)
            converted_list.append(converted_item)
        return type(data)(converted_list)
    else:
        # if it's other type, don't process
        return data


def _get_empty_data_structure(data_type: type | None) -> dict | list | tuple | set | None:
    if data_type is None:
        return None
    types = (dict, list, tuple, set)
    if data_type in types:
        return data_type()
    else:
        raise TypeError(f"Unsupported data type {data_type}")


def _get_data(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(self, data: str | bytes = None, *args, **kwargs) -> Any:
        if not data:
            if not self.path:
                raise AssertionError('For loading data, please provide the data or file path.')
            try:
                data = Path(self.path).read_bytes()
            except FileNotFoundError:  # when file not found
                return _get_empty_data_structure(self.data_type)
        return func(self, data, *args, **kwargs)
    return wrapper


def _dump(self: Any, data: bytes | str) -> bytes | str:
    if self.path:
        if isinstance(data, str):
            Path(self.path).write_text(data, encoding=self.encoding)
        else:
            Path(self.path).write_bytes(data)
    return data


class Serializer:
    def __init__(self, path: str | Path = None, encoding: str = 'utf-8', data_type: type = None):
        self.path, self.encoding, self.data_type = path, encoding, data_type

    @_get_data
    def _load(self, data: str | bytes, lib: ModuleType, **kwargs) -> Any:
        if lib in [json, yaml] and isinstance(data, bytes):
            data = data.decode(self.encoding)
        if lib is json:
            try:
                deserialized_data = json.loads(data, **kwargs)
            except json.decoder.JSONDecodeError:  # when data is empty
                return _get_empty_data_structure(self.data_type)
        elif lib is yaml:
            deserialized_data = yaml.safe_load(data)
        elif lib is pickle:
            try:
                deserialized_data = pickle.loads(data, **kwargs)
            except EOFError:  # when data is empty
                return _get_empty_data_structure(self.data_type)
        else:
            raise AssertionError
        return deserialized_data

    def load_yaml(self, data: str = None, **kwargs) -> Any:
        return self._load(data, yaml, **kwargs)

    def load_json(self, data: str = None, trans_key_to_num: bool = False, **kwargs) -> Any:
        json_data = self._load(data, json, **kwargs)
        if trans_key_to_num:
            return _convert_json_dict_key_to_number(json_data)
        return json_data

    def load_pickle(self, data: bytes = None, **kwargs) -> Any:
        return self._load(data, pickle, **kwargs)

    def dump_yaml(self, data: Any, allow_unicode: bool = True, **kwargs) -> str:
        string_io = io.StringIO()
        yaml.dump(data, string_io, allow_unicode=allow_unicode, **kwargs)
        data = string_io.getvalue()
        return _dump(self, data)

    def dump_json(self, data: Any, indent: int = 4, ensure_ascii: bool = False, minimum: bool = True, **kwargs) -> str:
        self_kwargs = {'ensure_ascii': ensure_ascii}
        if minimum:
            self_kwargs['separators'] = (',', ':')
        else:
            self_kwargs['indent'] = indent
        kwargs.update(self_kwargs)
        data = json.dumps(data, **kwargs)
        return _dump(self, data)

    def dump_pickle(self, data: Any, **kwargs) -> bytes:
        data = pickle.dumps(data, **kwargs)
        return _dump(self, data)


class CompressSerializer:
    _UNCOMPRESSED, _COMPRESSED = '0', '1'
    _ZLIB, _LZMA = '0', '1'
    _JSON, _PICKLE, _YAML = '00', '01', '10'
    _LIB_DICT = {_ZLIB: Compressor.ZLIB, _LZMA: Compressor.LZMA}
    _FORMAT_DICT = {_JSON: 'json', _PICKLE: 'pickle', _YAML: 'yaml'}
    AUTO = 'auto'

    class _Metadata:
        _ACCESS_DICT = {'compressed': (0, 1), 'lib': (1, 2), 'format': (2, 4)}

        def __init__(self, metadata: int | bytes = 0):
            self.bm = BitManipulator(metadata, fixed_bits=8)

        def _get(self, start: int, stop: int) -> str:
            return self.bm[start:stop]

        def _set(self, start: int, stop: int, value: str) -> None:
            self.bm[start:stop] = value

        def __getattr__(self, name):
            if name in self._ACCESS_DICT:
                return self._get(*self._ACCESS_DICT[name])
            return super().__getattribute__(name)

        def __setattr__(self, name, value):
            if name in self._ACCESS_DICT:
                return self._set(*self._ACCESS_DICT[name], value)
            super().__setattr__(name, value)

    def __init__(self, path: str | Path = None, encoding: str = 'utf-8', data_type: type = None,
                 compress: bool | str = AUTO, threshold: int = 1024 * 128, compress_lib: str = Compressor.ZLIB):
        """When the data length is greater than the threshold, will execute compression"""
        self.path, self.encoding, self.data_type = path, encoding, data_type
        self.compress, self.threshold, self.compress_lib = compress, threshold, compress_lib
        self._c = Compressor(lib=self.compress_lib)
        self._s = Serializer(encoding=self.encoding, data_type=self.data_type)

    def _get_uncompressed_data_and_format(self, data: bytes) -> tuple[bytes, str]:
        metadata = self._Metadata(data[0])
        data = data[1:]
        if metadata.compressed == self._COMPRESSED:
            data = self._c.decompress(data, lib=self._LIB_DICT[metadata.lib])
        return data, metadata.format

    @_get_data
    def load(self, data: bytes = None, *args, **kwargs) -> Any:
        uncompressed_data, format = self._get_uncompressed_data_and_format(data)
        return getattr(self._s, f'load_{self._FORMAT_DICT[format]}')(uncompressed_data, *args, **kwargs)

    @_get_data
    def load_pickle(self, data: bytes = None, **kwargs) -> Any:
        return self._s.load_pickle(self._get_uncompressed_data_and_format(data)[0], **kwargs)

    @_get_data
    def load_json(self, data: bytes = None, trans_key_to_num: bool = False, **kwargs) -> Any:
        return self._s.load_json(self._get_uncompressed_data_and_format(data)[0].decode(encoding=self.encoding),
                                 trans_key_to_num, **kwargs)

    @_get_data
    def load_yaml(self, data: bytes = None, **kwargs) -> Any:
        return self._s.load_yaml(self._get_uncompressed_data_and_format(data)[0].decode(encoding=self.encoding),
                                 **kwargs)

    def _compress_or_not(self, data: bytes, compress: bool | None) -> bool:
        if compress is None:  # if None, depends on self.compress
            if self.compress == self.AUTO and len(data) > self.threshold:
                return True
            return bool(self.compress)
        return bool(compress)

    def _get_compressed_data(self, data: bytes, compress: bool | None, format: str) -> bytes:
        metadata = self._Metadata()
        metadata.format = format
        metadata.lib = get_key_from_value(self._LIB_DICT, self.compress_lib)

        compress = self._compress_or_not(data, compress)
        if compress:
            metadata.compressed = self._COMPRESSED
            data = self._c.compress(data)
        else:
            metadata.compressed = self._UNCOMPRESSED
        return _dump(self, metadata.bm.to_bytes() + data)

    def dump_pickle(self, data: Any, compress: bool | None = None, **kwargs) -> bytes:
        return self._get_compressed_data(self._s.dump_pickle(data, **kwargs), compress, self._PICKLE)

    def dump_json(self, data: Any, compress: bool | None = None,
                  indent: int = 4, ensure_ascii: bool = False, minimum: bool = True, **kwargs) -> bytes:
        data = self._s.dump_json(data, indent, ensure_ascii, minimum, **kwargs)
        return self._get_compressed_data(data.encode(encoding=self.encoding), compress, self._JSON)

    def dump_yaml(self, data: Any, compress: bool | None = None, allow_unicode: bool = True, **kwargs) -> bytes:
        data = self._s.dump_yaml(data, allow_unicode, **kwargs)
        return self._get_compressed_data(data.encode(encoding=self.encoding), compress, self._YAML)
