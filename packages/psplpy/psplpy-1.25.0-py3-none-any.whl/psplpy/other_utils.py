import datetime
import io
import math
import multiprocessing
import platform
import random
import re
import string
import sys
import time
from abc import ABC, abstractmethod
from typing import Any, Type, Union
import json
import os
from pathlib import Path
import cv2
import numpy as np
from PIL import ImageGrab, Image


class OutputCapture:
    def __init__(self):
        self._original_stdout = sys.stdout
        self._original_stderr = sys.stderr
        self._captured_stdout = io.StringIO()
        self._captured_stderr = io.StringIO()
        self.restart_capture()

    def restart_capture(self):
        sys.stdout = self._captured_stdout
        sys.stderr = self._captured_stderr

    def stop_capture(self):
        sys.stdout = self._original_stdout
        sys.stderr = self._original_stderr

    def get_stdout(self) -> str:
        return self._captured_stdout.getvalue()

    def get_stderr(self) -> str:
        return self._captured_stderr.getvalue()

    def get_output(self) -> tuple[str, str]:
        return self.get_stdout(), self.get_stderr()

    def get_output_and_stop(self) -> tuple[str, str]:
        self.stop_capture()
        return self.get_stdout(), self.get_stderr()

    def clear_stdout(self):
        self._captured_stdout.truncate(0)
        self._captured_stdout.seek(0)

    def clear_stderr(self):
        self._captured_stderr.truncate(0)
        self._captured_stderr.seek(0)

    def clear(self):
        self.clear_stdout()
        self.clear_stderr()


class InputMock:
    def __init__(self, auto_line_wrapping: bool = False):
        self.auto_line_wrapping = auto_line_wrapping
        self.original_stdin = sys.stdin

    def input(self, s: str) -> None:
        if self.auto_line_wrapping:
            s += '\n'
        sys.stdin = io.StringIO(s)

    def restore(self) -> None:
        sys.stdin = self.original_stdin


class ClassProperty:
    """A decorator similar to 'property', but with the ability to use the class to access it,
       and the 'fget' method receives the class as its argument, rather than an instance"""
    def __init__(self, fget=None):
        self.fget = fget

    def __set_name__(self, owner, name):
        self._name = name

    def getter(self, fget):
        self.fget = fget
        return self

    def __get__(self, instance, owner: type) -> Any:
        if self.fget is None:
            raise AttributeError(f"can't read attribute '{self._name}'")
        return self.fget(owner)


class FunctionClass(ABC):
    def __new__(cls, *args, **kwargs) -> Any:
        instance = super().__new__(cls)
        instance._init()
        return instance(*args, **kwargs)

    def _init(self) -> None: ...

    @abstractmethod
    def __call__(self, *args, **kwargs): ...


class is_sys(FunctionClass):
    WINDOWS = 'Windows'
    LINUX = 'Linux'
    MACOS = 'Darwin'

    def __new__(cls, os_name: str) -> bool:
        return super().__new__(cls, os_name)

    def __call__(self, os_name: str) -> bool:
        this_os_name = platform.system()
        if os_name == this_os_name:
            return True
        return False


def recursive_convert(data: list | tuple, to: Type) -> tuple | list:
    """Recursively convert the lists and tuples are nested within each other to only tuples or lists"""
    if isinstance(data, (list, tuple)):
        return to(recursive_convert(item, to=to) for item in data)
    return data


def split_list(lst: list, n: int) -> list[list]:
    """Split a list into n equal length sublists in original order"""
    size = len(lst) // n
    remainder = len(lst) % n

    result_lists = []
    start = 0

    for i in range(n):
        if i < remainder:
            end = start + size + 1
        else:
            end = start + size

        result_lists.append(lst[start:end])
        start = end

    return result_lists


def get_key_from_value(dct: dict, value: Any, find_all: bool = False,
                       allow_null: bool = False) -> Union[Any, None]:
    keys = []
    for key, val in dct.items():
        if val == value:
            if not find_all:
                return key
            keys.append(key)
    if not keys:
        if allow_null:
            return None
        raise KeyError(f"No corresponding key exists")
    return keys


class get_env(FunctionClass):
    env_file = '.env'

    @staticmethod
    def _parse_key_value() -> None:
        result = {}
        lines = Path(get_env.env_file).read_text(encoding='utf-8').strip().split('\n')
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#'):
                key_value = line.split('=', maxsplit=2)
                result[key_value[0].strip()] = key_value[1].strip()
        for key, value in result.items():
            os.environ[key] = value

    def _init(self) -> None:
        self._has_read = False

    def __new__(cls, env_name: str, reload: bool = False, not_json: bool = False) -> Any:
        return super().__new__(cls, env_name, reload, not_json)

    def __call__(self, env_name: str, reload: bool = False, not_json: bool = False) -> Any:
        if reload:
            self._parse_key_value()
        env = os.environ.get(env_name)
        try:
            if not_json:
                return env
            return json.loads(env)
        except json.decoder.JSONDecodeError:
            return env
        except TypeError:
            if self._has_read:
                raise KeyError(f'Environment variable {env_name} not exist.')
            self._parse_key_value()
            self._has_read = True
            return self.__call__(env_name, reload, not_json)


class PerfCounter:
    US = 'us'
    MS = 'ms'
    S = 's'
    disabled = False

    def __init__(self, unit: str = MS, places: int = 4):
        if not self.disabled:
            self.unit = unit
            self.places = places

            self._start = time.perf_counter()

    def refresh(self) -> None:
        if not self.disabled:
            self._start = time.perf_counter()

    def elapsed(self) -> float:
        if not self.disabled:
            elapsed = time.perf_counter() - self._start
            if self.unit == self.MS:
                elapsed = elapsed * 1000
            elif self.unit == self.US:
                elapsed = elapsed * 1000 * 1000
            self.refresh()
            return elapsed
        return 0

    def show(self, tag: str = '') -> None:
        if not self.disabled:
            if tag:
                tag = tag + ': '
            print(f'{tag}{self.elapsed():.{self.places}f}{self.unit}')
            self.refresh()


class Timer:
    def __init__(self, interval: float = 0, warning_multiple: float = 0, error_multiple: float = 0):
        self._interval = interval
        self._warning_multiple = warning_multiple
        self._error_multiple = error_multiple

        self._cycle_count = 0
        self._very_start = time.time()

    def wait(self) -> None:
        self._cycle_count += 1
        sleep_time = self._very_start + self._cycle_count * self._interval - time.time()
        if sleep_time > 0:
            time.sleep(sleep_time)
        else:
            if self._warning_multiple > 0 and -sleep_time > self._warning_multiple * self._interval:
                sys.stderr.write(f"Warning, current delay: {-sleep_time:.2f}s\n")
            if self._error_multiple > 0 and -sleep_time > self._error_multiple * self._interval:
                raise TimeoutError(f'Current delay: {-sleep_time:.2f}s')


class TimeoutChecker:
    instances = {}

    def __new__(cls, timeout_seconds: float, unique_id: Any = None):
        if unique_id in cls.instances:
            cls.instances[unique_id]['is_first_created'] = False
            return cls.instances[unique_id]['instance']
        else:
            instance = super().__new__(cls)
            cls.instances[unique_id] = {'instance': instance, 'is_first_created': True}
            return instance

    def __init__(self, timeout_seconds: float, unique_id: Any = None):
        """unique_id is required when two or more instances existing simultaneously, e.g. using threading"""
        self.unique_id = unique_id
        if self.instances[self.unique_id]['is_first_created']:
            self.timeout_seconds = timeout_seconds
            self.start_time = time.time()

    def _delete_instance(self):
        if self.unique_id in self.instances:
            del self.instances[self.unique_id]

    def ret_false(self) -> bool:
        current_time = time.time()
        if current_time - self.start_time > self.timeout_seconds:
            self._delete_instance()
            return False
        return True

    def raise_err(self, error_type: Type = None) -> bool:
        if not self.ret_false():
            if not error_type:
                message = (f'Start at {time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.start_time))}, '
                           f'after {self.timeout_seconds}s time out')
                raise TimeoutError(message)
            raise error_type()
        return True


class ScreenShotMaker:
    PNG = 'png'  # using PIL saves to png, the smallest size, but the longest time
    BMP = 'bmp'  # using PIL saves to bmp, the biggest size, but the shortest time
    PNG_OPENCV = 'png_opencv'  # using opencv saves to png, medium size and time

    def __init__(self, region: (int, int, int, int) = None, fps: float = 10, save_dir: str | Path = None,
                 show_info: bool = True, enable_warning: bool = True, savers_num: int | str = 'auto',
                 save_to: str = PNG_OPENCV) -> None:
        self._region, self._fps, self._show_info = region, fps, show_info
        self._enable_warning, self._save_to = enable_warning, save_to

        self._interval = 1 / self._fps
        self._savers_num = self._get_savers_num(savers_num)
        self._frame_counter, self._frame_queue = 0, multiprocessing.Queue()

        self._save_dir = Path(save_dir) if save_dir is not None else Path().cwd()
        self._save_dir = self._save_dir / f'{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S_%f")}'
        self._save_dir.mkdir(parents=True, exist_ok=True)

        self._start_savers()
        self._screenshot()

    def _get_savers_num(self, savers_num: int | str) -> int:
        if savers_num == 'auto':
            if self._save_to == self.PNG:
                savers_num = self._fps
            elif self._save_to == self.BMP:
                savers_num = math.ceil(self._fps / 10)
            elif self._save_to == self.PNG_OPENCV:
                savers_num = math.ceil(self._fps / 3)
        return savers_num

    def _warning(self, lag: float) -> None:
        if self._enable_warning and lag > self._interval:
            print(f'Warning - {datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S.%f")} - '
                  f'frame {self._frame_counter} - the lag is {lag:.3f}s')
        if self._enable_warning and self._frame_queue.qsize() > self._fps:
            print(f'Warning - {datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S.%f")} - '
                  f'frame {self._frame_counter} - the queue size is {self._frame_queue.qsize()}')

    @staticmethod
    def _timer(func):
        def wrapper(self, *args, **kwargs):
            t_start = time.perf_counter()
            while True:
                expected_time = t_start + self._frame_counter * self._interval
                current_time = time.perf_counter()
                lag = current_time - expected_time
                if current_time > expected_time:
                    self._warning(lag)
                    result = func(self, *args, **kwargs)
                    self._frame_queue.put({'time': current_time, 'result': result, 'counter': self._frame_counter})
                    self._frame_counter += 1
                else:
                    time.sleep(0.001)
        return wrapper

    @_timer
    def _screenshot(self):
        return ImageGrab.grab(self._region)

    def _save(self, image: Image.Image, path: str):
        if self._save_to == self.PNG_OPENCV:
            image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            cv2.imwrite(f'{path}.png', image)
        elif self._save_to == self.PNG:
            image.save(f'{path}.png')
        elif self._save_to == self.BMP:
            image.save(f'{path}.bmp')
        else:
            raise AssertionError

    def _saver(self, frame_queue: multiprocessing.Queue):
        while True:
            if not frame_queue.empty():
                frame = frame_queue.get()
                self._save(frame['result'], str(self._save_dir / f'{frame["time"]:.2f}'))
                if self._show_info:
                    print(f'At {frame["time"]:.3f}, save frame {frame["counter"]}')
            else:
                time.sleep(0.01)

    def _start_savers(self):
        for _ in range(self._savers_num):
            multiprocessing.Process(target=self._saver, args=(self._frame_queue,)).start()


def overlay_print(s: str) -> None:
    sys.stdout.write(f'\r{s}')  # \r means go back to the beginning of the line
    sys.stdout.flush()


def progress_bar(progress: float, show_str: str = '', bar_length: int = 40,
                 finished_chr: str = '=', unfinished_chr: str = '-',
                 left_border_chr: str = '[', right_border_chr: str = ']',
                 progress_precision: int = 2) -> None:
    if progress > 1:
        progress = 1
    filled_length = int(progress * bar_length)
    bar = finished_chr * filled_length + unfinished_chr * (bar_length - filled_length)
    show_str = show_str if show_str else f'{progress * 100:.{progress_precision}f}%'
    overlay_print(f'{left_border_chr}{bar}{right_border_chr} {show_str}')


def limited_input(str_list: [list | tuple | set] = None, regex_list: [list | tuple | set] = None,
                  func_list: [list | tuple | set] = None, input_processing_func=None,
                  print_str: str = '', error_tip: str = 'Invalid input, please re-enter.') -> str:
    result_str = ''
    while True:
        input_str = input(print_str + '\n')
        if str_list:
            if input_str in str_list:
                result_str = input_str
        if not result_str and regex_list:
            for regex in regex_list:
                if re.match(regex, input_str):
                    result_str = input_str
                    break
        if not result_str and func_list:
            for func in func_list:
                if func(input_str):
                    result_str = input_str
                    break
        if result_str:
            if input_processing_func:
                return input_processing_func(result_str)
            return result_str
        print(error_tip)


class VideoToFrames:
    def __init__(self, video_path: str | Path, save_dir: str | Path = '', frame_interval: int = 1,
                 show_progress: bool = True, workers: int = 5) -> None:
        self.video_path = video_path
        self.save_dir = Path(save_dir) / Path(video_path).stem
        self.save_dir.mkdir(parents=True, exist_ok=True)
        self.frame_interval = frame_interval
        self.show_progress = show_progress
        self._progress = multiprocessing.Value('i', 0)
        self.workers = workers

        cap = cv2.VideoCapture(self.video_path)
        self.total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.num_digits = len(str(self.total_frames))  # 计算帧数的填充位数

        indices = self._split_number_into_parts(self.total_frames, self.workers)
        for i in range(self.workers):
            multiprocessing.Process(target=self._save_process, args=(indices[i], indices[i + 1])).start()

    @staticmethod
    def _split_number_into_parts(number: int, parts: int) -> list[int]:
        if parts <= 0 or number <= 0 or not isinstance(parts, int) or not isinstance(number, int):
            raise ValueError("Number and parts should be int and greater than 0.")
        part_size = number // parts
        return [i * part_size for i in range(parts)] + [number]

    def _save_process(self, start_frame: int, stop_frames: int) -> None:
        cap = cv2.VideoCapture(self.video_path)
        while start_frame < stop_frames:
            ret, frame = cap.read()
            if start_frame % self.frame_interval == 0:
                frame_filename = self.save_dir / f"frame_{start_frame:0{self.num_digits}d}.png"
                cv2.imwrite(str(frame_filename), frame)

            start_frame += 1
            with self._progress.get_lock():
                self._progress.value += 1
                if self.show_progress:
                    progress_bar(self._progress.value / self.total_frames,
                                 show_str=f'{self._progress.value}/{self.total_frames}')
        cap.release()


def gen_passwd(length: int = 15, has_upper: bool = True, has_lower: bool = True,
               has_digits: bool = True, has_special: bool = True) -> str:
    characters = ''

    if has_upper:
        characters += string.ascii_uppercase
    if has_lower:
        characters += string.ascii_lowercase
    if has_digits:
        characters += string.digits
    if has_special:
        characters += string.punctuation
    if not characters:
        raise ValueError("No characters were selected")

    while True:
        password = ''.join(random.choice(characters) for _ in range(length))

        # check whether every character type in the password
        if (not has_upper or any(c.isupper() for c in password)) and \
                (not has_lower or any(c.islower() for c in password)) and \
                (not has_digits or any(c.isdigit() for c in password)) and \
                (not has_special or any(c in string.punctuation for c in password)):
            return password
