import random
from tests.__init__ import *
from psplpy.serialization_utils import *
from psplpy.other_utils import PerfCounter


def test_bit_manipulator():
    bm0, bm1, bm256 = BitManipulator(0, max_bits=8), BitManipulator(1), BitManipulator(256)
    # test __len__
    assert len(bm0) == 0, len(bm256) == 9
    # test __setitem__
    bm0[7] = 1
    bm256[15] = 1
    assert bm0.bit_value == 0b10000000 and bm256.bit_value == 0b10000001_00000000
    bm0[1:8:2] = '1001'
    assert str(bm0) == '10000010', str(bm0)
    try:
        bm0[9:10] = '11'
    except ValueError as e:
        print(e)
    else:
        assert False
    try:
        bm0[0] = '11'
    except ValueError as e:
        print(e)
    else:
        assert False
    bm1[9:11] = '11'    # out of the original bit range
    assert bm1.bit_value == 0b110_00000001
    # test max_bits
    try:
        bm0.set_bit(8, 1)
    except ValueError as e:
        print(e)
    else:
        assert False
    try:
        bm0.set_bit(8, 0)
    except ValueError as e:
        assert False
    # test _index_check, __getitem__
    try:
        _ = bm0[-9]
    except IndexError as e:
        print(e)
    else:
        assert False
    assert str(bm0) == '10000010'
    assert bm0[128:256] == '0' * 128    # ability to slice out of range
    assert bm0[1024] == '0'
    assert bm0[7] == '1'
    assert bm0[4:8] == '0001'
    # test to_bytes
    b = bm0.to_bytes()
    assert b == b'\x82'
    assert bin(int.from_bytes(b, byteorder='big'))[2:] == '10000010'
    # test __format__
    assert bm0.__format__('o') == '202'
    assert bm0.__format__('x') == '82'
    assert bm0.__format__('d') == '130'
    # test __iter__
    assert ''.join([b for b in bm0]) == '10000010'[::-1]
    # test __lt__ __ne__ __ge__
    assert bm0 < bm256
    assert bm0 != bm256
    assert bm0 >= BitManipulator(bm0)
    # test fixed_bits
    bm = BitManipulator(0, fixed_bits=14)
    try:
        bm.set_bit(16, 1)
    except ValueError as e:
        print(e)
    else:
        assert False
    try:
        bm.set_bit(16, 0)
    except ValueError as e:
        assert False
    assert bm.to_bytes() == b'\x00\x00'
    assert bm.to_bytes(3) == b'\x00\x00\x00'
    assert BitManipulator(0).to_bytes() == b''
    assert str(bm) == '0' * 14, str(bm)
    assert bm.__format__('x') == '0'


bench_data = {}
rand_round = 10000
for i in range(rand_round):
    bench_data[str(random.randint(0, rand_round))] = random.uniform(0, rand_round)
python_data = {1: '100', 2: 200, 3: ['你好', [3.14, None, False]]}
json_str = '{"1":"100","2":200,"3":["你好",[3.14,null,false]]}'
pickle_bytes = (b'\x80\x04\x95/\x00\x00\x00\x00\x00\x00\x00}\x94(K\x01\x8c\x03100\x94K\x02K\xc8K\x03]\x94('
                b'\x8c\x06\xe4\xbd\xa0\xe5\xa5\xbd\x94]\x94(G@\t\x1e\xb8Q\xeb\x85\x1fN\x89eeu.')
yaml_str = "1: '100'\n2: 200\n3:\n- 你好\n- - 3.14\n  - null\n  - false\n"


def test_compress_serializer():
    zlib_serializer = CompressSerializer(threshold=1)
    lzma_serializer = CompressSerializer(threshold=1, compress_lib=Compressor.LZMA)

    p = PerfCounter()
    serialized_data = zlib_serializer.dump_pickle(bench_data)
    print(f'len: {len(serialized_data)},\t elapsed: {p.elapsed():.4f}ms,\t zlib_pickle')
    serialized_data = lzma_serializer.dump_pickle(bench_data)
    print(f'len: {len(serialized_data)},\t elapsed: {p.elapsed():.4f}ms,\t lzma_pickle')

    for dump, load, load_kwargs in [('dump_pickle', 'load_pickle', {}), ('dump_yaml', 'load_yaml', {}),
                                    ('dump_json', 'load_json', {'trans_key_to_num': True})]:
        dumps_data = getattr(zlib_serializer, dump)(python_data)
        assert isinstance(dumps_data, bytes), dump
        loads_data = getattr(zlib_serializer, load)(dumps_data, **load_kwargs)
        assert loads_data == python_data, f'{load}, {loads_data}'

    dumps_data = zlib_serializer.dump_pickle(python_data)
    assert zlib_serializer.load(dumps_data) == python_data
    dumps_data = zlib_serializer.dump_json(python_data)
    assert zlib_serializer.load(dumps_data, trans_key_to_num=True) == python_data


    compress_serializer = CompressSerializer(path=tmp_file, data_type=dict, compress=True)
    uncompress_serializer = CompressSerializer(path=tmp_file, data_type=dict, compress=False)

    for serializer in [compress_serializer, uncompress_serializer]:
        try:
            print(f'compress: {serializer.compress}')
            loads_data = serializer.load_json()
            assert loads_data == dict(), loads_data
            loads_data = serializer.load_json()
            assert loads_data == dict(), loads_data

            dumps_data = serializer.dump_json(python_data)
            assert isinstance(dumps_data, bytes)
            loads_data = serializer.load_json(trans_key_to_num=True)
            assert loads_data == python_data, loads_data

            dumps_data = serializer.dump_yaml(python_data)
            assert isinstance(dumps_data, bytes)
            loads_data = serializer.load_yaml()
            assert loads_data == python_data, loads_data

            dumps_data = serializer.dump_pickle(python_data)
            assert isinstance(dumps_data, bytes)
            loads_data = serializer.load_pickle()
            assert loads_data == python_data, loads_data
        finally:
            tmp_file.unlink(missing_ok=True)


def test_serializer():
    serializer = Serializer()
    p = PerfCounter()
    serialized_data = serializer.dump_pickle(bench_data)
    print(f'len: {len(serialized_data)},\t elapsed: {p.elapsed():.4f}ms,\t dumps_pickle')
    serialized_data = serializer.dump_json(bench_data)
    print(f'len: {len(serialized_data)},\t elapsed: {p.elapsed():.4f}ms,\t dumps_json')
    serialized_data = serializer.dump_yaml(bench_data)
    print(f'len: {len(serialized_data)},\t elapsed: {p.elapsed():.4f}ms,\t dumps_yaml')

    dumps_data = serializer.dump_json(python_data, ensure_ascii=False)
    loads_data = serializer.load_json(dumps_data, trans_key_to_num=True)
    assert dumps_data == json_str, dumps_data
    assert loads_data == python_data, loads_data

    dumps_data = serializer.dump_pickle(loads_data)
    loads_data = serializer.load_pickle(dumps_data)
    assert dumps_data == pickle_bytes, loads_data
    assert loads_data == python_data, loads_data

    dumps_data = serializer.dump_yaml(python_data)
    loads_data = serializer.load_yaml(dumps_data)
    assert dumps_data == yaml_str, dumps_data
    assert loads_data == python_data

    try:
        serializer = Serializer(path=tmp_file, data_type=dict)
        loads_data = serializer.load_json()
        assert loads_data == dict(), loads_data

        dumps_data = serializer.dump_json(python_data)
        assert dumps_data == json_str, dumps_data
        loads_data = serializer.load_json(trans_key_to_num=True)
        assert loads_data == python_data, loads_data

        dumps_data = serializer.dump_yaml(python_data)
        assert dumps_data == yaml_str, dumps_data
        loads_data = serializer.load_yaml()
        assert loads_data == python_data, loads_data

        dumps_data = serializer.dump_pickle(python_data)
        assert dumps_data == pickle_bytes, dumps_data
        loads_data = serializer.load_pickle()
        assert loads_data == python_data, loads_data
    finally:
        tmp_file.unlink(missing_ok=True)

    # test json encoder decoder
    class A:
        def __init__(self, a):
            self.a = a

        class AEncoder(json.JSONEncoder):
            def default(self, obj):
                if isinstance(obj, A):
                    return {'a': obj.a}
                return super().default(obj)

        class ADecoder(json.JSONDecoder):
            def __init__(self):
                super().__init__(object_hook=self._decode_a)

            @staticmethod
            def _decode_a(dct):
                return A(a=dct['a'])

    a_obj = A([100])
    encoded_str = Serializer().dump_json(a_obj, cls=A.AEncoder)
    assert encoded_str == '{"a":[100]}'
    decoded_a_obj = Serializer().load_json(encoded_str, cls=A.ADecoder)
    assert decoded_a_obj.a == a_obj.a


def tests():
    test_bit_manipulator()
    test_serializer()
    test_compress_serializer()


if __name__ == '__main__':
    tests()
