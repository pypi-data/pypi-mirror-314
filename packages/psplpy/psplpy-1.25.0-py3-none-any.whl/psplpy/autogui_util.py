import threading
import time
import pyautogui
import pyperclip
from pynput.keyboard import Controller, Key
from psplpy.concurrency_utils import ThreadLocks
from psplpy.network_utils import ServerSocket, ClientSocket


pyautogui.FAILSAFE = False
keyboard = Controller()


class AutoGui:
    def paste(self, s: str, pos: tuple[int, int] = (), desktop_pos: tuple[int, int] = (pyautogui.size()[0], 0)):
        for i in range(2):
            pyperclip.copy(s)
            pyautogui.click(*desktop_pos)
            time.sleep(0.1)
            pyautogui.click(*pos)
            time.sleep(0.1)
        keyboard.press(Key.ctrl)
        keyboard.press('v')
        time.sleep(0.1)
        pyautogui.click(1, 1)
        time.sleep(0.1)
        keyboard.release(Key.ctrl)
        keyboard.release('v')

    @staticmethod
    def drag_from(start_x: int, start_y: int, end_x: int, end_y: int, duration: float = 1):
        pyautogui.moveTo(start_x, start_y)
        return pyautogui.dragTo(end_x, end_y, duration=duration)


class AutoGuiCommand:
    def __init__(self, command: str, args: tuple | list, kwargs: dict, id: int, send_time: float):
        self.command = command
        self.args = args
        self.kwargs = kwargs
        self.id = id
        self.send_time = send_time  # the time when the command is sent
        self.exec_time = 0  # the execution time of the command
        self.result = None
        self.elapsed = 0  # the elapsed time between sending command and receiving result

    @property
    def tour_time(self) -> float:  # the time of network latency
        return self.elapsed - self.exec_time

    def __str__(self):
        return f"{str(self.__dict__)[:-1]}, 'tour_time': {self.tour_time}}}"

    __repr__ = __str__


class AutoGuiCommandNotFoundError(Exception):
    def __init__(self, command: str):
        self.command = command

    def __str__(self):
        return f"AutoGuiCommand not found: {self.command}"


class AutoGuiSender:
    def __init__(self, host: str = '127.0.0.1', port: int = 12345):
        self._client_socket = ClientSocket(host=host, port=port)
        self._client_socket.connect()
        self._id = 0

    def send(self, command: str, args: tuple | list = None, kwargs: dict = None) -> AutoGuiCommand:
        ac = AutoGuiCommand(command, args or (), kwargs or {}, self._id, time.time())
        self._id += 1
        self._client_socket.send_pickle(ac)
        ac: AutoGuiCommand = self._client_socket.recv_pickle()
        ac.elapsed = time.time() - ac.send_time
        if isinstance(ac.result, Exception):
            raise ac.result
        return ac


class AutoGuiExecutor:
    KM_LOCK = '_keyboard_and_mouse_lock'

    def __init__(self, host: str = '0.0.0.0', port: int = 12345):
        self._locks = ThreadLocks()
        self._locks.set_lock(self.KM_LOCK, auto_release_time=300)
        self._autogui = AutoGui()
        self._server_socket = ServerSocket(host=host, port=port)

    def run(self, new_thread: bool = False) -> None:
        if new_thread:
            threading.Thread(target=self._server_socket.handle, args=(self._handler,)).start()
        else:
            self._server_socket.handle(self._handler)

    def _handler(self, client_socket: ClientSocket, address):
        objs_require_km = [self._autogui, pyautogui]
        while True:
            ac: AutoGuiCommand = client_socket.recv_pickle()
            if not ac:
                break
            t_start = time.perf_counter()
            for obj in [self._locks, *objs_require_km]:
                if ac.command in dir(obj):
                    if obj in objs_require_km:
                        self._locks.acquire_lock(self.KM_LOCK)
                    result = getattr(obj, ac.command)(*ac.args, **ac.kwargs)
                    if obj in objs_require_km:
                        self._locks.release_lock(self.KM_LOCK)
                    break
            else:
                result = AutoGuiCommandNotFoundError(ac.command)
            ac.exec_time = time.perf_counter() - t_start
            ac.result = result
            client_socket.send_pickle(ac)
