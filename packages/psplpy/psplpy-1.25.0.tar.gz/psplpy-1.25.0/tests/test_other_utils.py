import io
import re
import time
from threading import Thread
from tests.__init__ import *
from psplpy.other_utils import *


def test_output_capture():
    capture = OutputCapture()
    print("This is stdout1")
    print("This is stdout2")
    print("This is stderr", file=sys.stderr)
    # test get_output() and stop_capture()
    stdout, stderr = capture.get_output_and_stop()
    assert stdout == "This is stdout1\nThis is stdout2\n", stdout
    assert stderr == "This is stderr\n", stderr
    # test after clear(), get two empty strings
    capture.clear()
    stdout, stderr = capture.get_output()
    assert stdout == '', stdout
    assert stderr == '', stderr
    # test cannot get anything after stop_capture() and will output on console
    print("This is stdout")
    print("This is stderr", file=sys.stderr)
    assert stdout == '', stdout
    assert stderr == '', stderr
    # test can capture after restart_capture()
    capture.restart_capture()
    print("This is stdout")
    print("This is stderr", file=sys.stderr)
    stdout, stderr = capture.get_output_and_stop()
    assert stdout == "This is stdout\n", stdout
    assert stderr == "This is stderr\n", stderr


def test_input_mock():
    input_mock = InputMock()
    # test normal input
    input_mock.input('hello')
    assert input() == 'hello'
    input_mock.input('hello\n\n\n')
    assert input() == 'hello'
    # test the EOFError will occur when input an empty string
    try:
        input_mock.input('')
        input()
    except EOFError as e:
        print(str(e))
    else:
        assert False
    # test the EOFError will not occur when set auto_line_wrapping=True
    input_mock = InputMock(auto_line_wrapping=True)
    try:
        input_mock.input('')
    finally:
        assert input() == ''
    # restore the stdin
    input_mock.restore()


def test_class_property():
    class Config:
        PROJECT_DIR = Path(__file__).parent.parent

        @ClassProperty
        def SRC_DIR(cls):
            return cls.PROJECT_DIR / 'src'

        @ClassProperty
        def DATA_DIR(cls):
            return cls.PROJECT_DIR / 'data'

    # test whether the 'ClassProperty' can return the correct value
    assert Config.SRC_DIR == Path('/home/a/src/psplpyProject/src')
    # test assigning a new variable, thus hiding the 'ClassProperty' instance
    Config.SRC_DIR = Path(__file__).parent
    assert Config.SRC_DIR == Path('/home/a/src/psplpyProject/tests')
    # test assigning a new 'ClassProperty' instance
    Config.SRC_DIR = ClassProperty(lambda cls: cls.PROJECT_DIR / '1')
    assert Config.SRC_DIR == Path('/home/a/src/psplpyProject/1')


def test_is_sys():
    assert is_sys(is_sys.LINUX) is True
    assert is_sys(is_sys.WINDOWS) is False


def test_recursive_convert():
    data = [1, (2, [3, 4])]
    assert recursive_convert(data, to=list) == [1, [2, [3, 4]]]
    assert recursive_convert(data, to=tuple) == (1, (2, (3, 4)))


def test_split_list():
    lst = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    assert split_list(lst, 4) == [[1, 2, 3], [4, 5], [6, 7], [8, 9]]


def test_get_key_from_value():
    dct = {'a': 1, 'b': 2, 'c': 1, 'd': 1}
    assert get_key_from_value(dct, 1) == 'a'
    assert get_key_from_value(dct, 2, find_all=True) == ['b']
    assert get_key_from_value(dct, 1, find_all=True) == ['a', 'c', 'd']
    assert get_key_from_value(dct, 3, allow_null=True) is None
    assert get_key_from_value(dct, 3, find_all=True, allow_null=True) is None
    try:
        get_key_from_value(dct, 3)
    except KeyError as e:
        print(e)
    else:
        assert False


def test_get_env():
    assert get_env('SERVICE') == 'psplpy'
    try:
        get_env('S')
    except KeyError as e:
        print(str(e))
    else:
        raise AssertionError


def test_perf_counter():
    p = PerfCounter()
    time.sleep(0.1)
    assert int(p.elapsed()) == int(0.1 * 1000)
    time.sleep(0.2)
    p.show('perf')


def test_timer():
    # basic test
    interval = 0.1
    timer = Timer(interval=interval)
    start_time = time.time()
    for i in range(10):
        timer.wait()
        elapsed = time.time() - start_time
        assert elapsed < (i + 2) * interval, elapsed
        print(elapsed)
    # test warning and error
    output_capture = OutputCapture()
    timer = Timer(interval=interval, warning_multiple=1, error_multiple=2)
    try:
        for i in range(1000):
            timer.wait()
            time.sleep(interval * 1.75)
    except TimeoutError as e:
        print(str(e))
        stdout, stderr = output_capture.get_output_and_stop()
        assert re.match(r'Current delay: 0\.2.s\n', stdout), repr(stdout)
        assert re.match(r'Warning, current delay: 0\.1.s\n'
                        r'Warning, current delay: 0\.2.s\n', stderr), repr(stderr)
    else:
        assert False


def test_timeout_checker():
    def checker(timeout: float, unique_id: Any = None, check_time: float = None,
                func: str = 'ret_false', end_loop_time: float = 10000):
        t_start = time.time()
        while getattr(TimeoutChecker(timeout, unique_id=unique_id), func)():
            if time.time() - t_start > end_loop_time:
                break
            time.sleep(0.01)
        print(time.time() - t_start)
        assert int(time.time() - t_start) == check_time or timeout

    Thread(target=checker, kwargs={'timeout': 1, 'unique_id': 1}).start()
    timeout = 2
    Thread(target=checker, kwargs={'timeout': 2, 'unique_id': 2}).start()
    time.sleep(timeout + 0.5)

    kwargs = {'timeout': 2, 'unique_id': 1, 'check_time': 1, 'func': 'raise_err', 'end_loop_time': 1}
    Thread(target=checker, kwargs=kwargs).start()
    try:
        checker(timeout=1, unique_id=2, func='raise_err')
    except Exception as e:
        assert isinstance(e, TimeoutError)


def test_screenshot_maker():
    pass
    # ScreenShotMaker()


def test_gen_passwd():
    print(gen_passwd())


def tests():
    print('test other utils')
    test_output_capture()
    test_input_mock()
    test_class_property()
    test_is_sys()
    test_recursive_convert()
    test_split_list()
    test_get_key_from_value()
    test_get_env()
    test_perf_counter()
    test_timer()
    test_timeout_checker()
    test_screenshot_maker()
    test_gen_passwd()


if __name__ == '__main__':
    tests()
