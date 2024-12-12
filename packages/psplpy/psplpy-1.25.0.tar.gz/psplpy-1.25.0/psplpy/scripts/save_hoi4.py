import shutil
import time
import traceback
from pathlib import Path
from typing import Callable, Any


def retry_func(func: Callable, args: tuple | list = None, kwargs: dict = None, max_attempts: int = 3,
               delay: float = 0, retry_exceptions: tuple | list = None, emit_tip: bool = False) -> Any:
    attempts = 0
    args, kwargs = args or (), kwargs or {}
    while max_attempts < 0 or attempts < max_attempts:
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            if retry_exceptions is None or any(isinstance(e, exc) for exc in retry_exceptions):
                if emit_tip:
                    print(f'{func.__name__} attempts {attempts} times, exception is {type(e).__name__}: {e}')
                attempts += 1
                time.sleep(delay)
            else:
                raise e
    raise Exception(f"Max retry attempts reached for function: {func.__name__}")


class SaveHoi4AutoSave:
    auto_save_file_dir = Path.home() / r'Documents\Paradox Interactive\Hearts of Iron IV\save games'
    auto_save_file_path = auto_save_file_dir / 'autosave.hoi4'

    def __init__(self, start_time: tuple = (36, 2), last_modified_time: float = time.time()):
        self.start_time = list(start_time)
        self.last_modified_time = last_modified_time
        self.monitor_file_modification()

    def monitor_file_modification(self):
        while True:
            modification_time = retry_func(self.auto_save_file_path.stat,
                                           delay=2, max_attempts=-1).st_mtime
            if modification_time > self.last_modified_time:
                self.last_modified_time = modification_time
                self.save()
                self.update_start_time()
            else:
                time.sleep(1)

    def save(self):
        file_name = f'19{self.start_time[0]}-{self.start_time[1]}_{int(time.time())}.hoi4'
        file_path = self.auto_save_file_dir / file_name
        retry_func(shutil.copy2, (self.auto_save_file_path, file_path), delay=1, emit_tip=True)
        print(f'Saved {file_name}')

    def update_start_time(self):
        self.start_time[1] += 1
        if self.start_time[1] == 13:
            self.start_time[1] = 1
            self.start_time[0] += 1


if __name__ == '__main__':
    try:
        s = SaveHoi4AutoSave(start_time=(36, 2))
    except Exception as e:
        traceback.print_exc()
        input()
