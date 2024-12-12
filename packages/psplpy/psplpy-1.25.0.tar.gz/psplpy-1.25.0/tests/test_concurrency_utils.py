from tests.__init__ import *
from psplpy.concurrency_utils import ThreadLocks


def tests():
    tl = ThreadLocks()
    lock_name = 'test'
    assert tl.has_lock(lock_name) is False
    assert tl.set_lock(lock_name, auto_release_time=1) is None
    assert tl.has_lock(lock_name) is True
    assert tl.locked(lock_name) is False
    assert tl.acquire_lock(lock_name) is True
    assert tl.locked(lock_name) is True
    assert tl.release_lock(lock_name) is None
    assert tl.locked(lock_name) is False
    print(tl.locks)

    assert tl.acquire_lock(lock_name) is True
    assert tl.acquire_lock(lock_name, timeout=0.1) is False
    print(tl.auto_release_info)
    time.sleep(1)
    assert tl.acquire_lock(lock_name, timeout=1) is True
    print(tl.auto_release_info)


if __name__ == '__main__':
    tests()
