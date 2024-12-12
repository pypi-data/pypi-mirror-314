import functools
import os
import re
from pathlib import Path
from typing import Callable
from typing import List, Union, Generator


def _path_operation(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(path: str | Path) -> str | Path:
        original_type = type(path)
        if isinstance(path, str):
            path = Path(path)
        elif not isinstance(path, Path):
            raise ValueError(f"Path must be a string or Path object, not {original_type}")

        new_path = func(path)

        if original_type is str:
            return str(new_path)
        return new_path

    return wrapper


@_path_operation
def auto_rename(path: str | Path) -> str | Path:
    """If the file name has existed, add (n) after the file name and return, or return the original name."""
    n = 0
    while path.exists():
        n += 1
        stem = re.sub(r"\(\d+\)$", "", path.stem)
        path = path.with_name(f'{stem}({n}){path.suffix}')
    return path


def get_file_paths(folder_path: str | Path, relative: bool = False, generator: bool = False, to_str: bool = False
                   ) -> Union[List[Path], List[str], Generator[str | Path, None, None]]:
    def _generate_file_paths() -> Generator[str | Path, None, None]:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if relative:
                    file_path = os.path.relpath(os.path.join(root, file), folder_path)
                else:
                    file_path = os.path.abspath(os.path.join(root, file))
                if not to_str:
                    file_path = Path(file_path)
                yield file_path

    if generator:
        return _generate_file_paths()
    else:
        return list(_generate_file_paths())
