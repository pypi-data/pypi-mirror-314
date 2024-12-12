from tests.__init__ import *
from psplpy.file_utils import *


def test_auto_rename():
    cat_path = rc_dir / 'cat.png'
    renamed_cat_path = str(cat_path).replace('.png', '(1).png')
    print(renamed_cat_path)
    assert auto_rename(cat_path) == Path(renamed_cat_path)
    assert auto_rename(str(cat_path)) == renamed_cat_path


def test_get_file_paths():
    folder_path = rc_dir / 'test_get_paths'

    abs_list = ['/home/a/src/psplpyProject/tests/resources/test_get_paths/test.txt',
                '/home/a/src/psplpyProject/tests/resources/test_get_paths/inner/inner_test.txt',
                '/home/a/src/psplpyProject/tests/resources/test_get_paths/inner/inner_test2.txt']
    rel_list = [Path('test.txt'), Path('inner/inner_test.txt'), Path('inner/inner_test2.txt')]

    paths_list = get_file_paths(folder_path, to_str=True)
    assert paths_list == abs_list, paths_list

    paths_list = get_file_paths(folder_path, relative=True)
    assert paths_list == rel_list, paths_list

    paths_list = get_file_paths(folder_path, generator=True, to_str=True)
    assert isinstance(paths_list, Generator), type(paths_list)
    assert list(paths_list) == abs_list


def tests():
    print('test file utils')
    test_auto_rename()
    test_get_file_paths()


if __name__ == '__main__':
    tests()
