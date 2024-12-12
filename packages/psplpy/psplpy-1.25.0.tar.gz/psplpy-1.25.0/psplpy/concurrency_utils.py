import argparse
import threading
import time


class ThreadLocks:
    def __init__(self):
        self.locks = argparse.Namespace()
        # lock_name: {'auto_release': bool, 'timeout': float, 'last_acquired_time': time.time}
        self.auto_release_info = {}

    def has_lock(self, lock_name: str) -> bool:
        return hasattr(self.locks, lock_name)

    def _get_lock(self, lock_name: str) -> threading.Lock:
        return getattr(self.locks, lock_name)

    def set_lock(self, lock_name: str, auto_release_time: float = -1) -> None:
        if self.has_lock(lock_name):
            raise AttributeError(f"{lock_name} has already existed")
        else:
            setattr(self.locks, lock_name, threading.Lock())
        if auto_release_time >= 0:
            info = {'auto_release': True, 'timeout': auto_release_time, 'last_acquired_time': 0}
            self.auto_release_info[lock_name] = info
            self._auto_release_daemon(lock_name)
        else:
            self.auto_release_info[lock_name] = {'auto_release': False}

    def acquire_lock(self, lock_name: str, blocking: bool = True, timeout: float = -1) -> bool:
        lock = self._get_lock(lock_name)
        acquire_result = lock.acquire(blocking=blocking, timeout=timeout)
        if acquire_result:
            self.auto_release_info[lock_name]['last_acquired_time'] = time.time()
        return acquire_result

    def release_lock(self, lock_name: str, ignore_released: bool = True) -> None:
        lock = self._get_lock(lock_name)
        if ignore_released and not self.locked(lock_name):
            return None
        return lock.release()

    def locked(self, lock_name: str) -> bool:
        lock = self._get_lock(lock_name)
        return lock.locked()

    def _auto_release_daemon(self, lock_name: str) -> None:
        def _d():
            auto_release_time = self.auto_release_info[lock_name]['timeout']
            inspect_interval = auto_release_time / 100
            while True:
                time.sleep(inspect_interval)
                if self.locked(lock_name):
                    if time.time() - self.auto_release_info[lock_name]['last_acquired_time'] >= auto_release_time:
                        self.release_lock(lock_name)

        daemon = threading.Thread(target=_d)
        daemon.daemon = True
        daemon.start()
