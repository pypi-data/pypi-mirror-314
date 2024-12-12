import asyncio
import functools
import json
import datetime
import multiprocessing
import queue
import sys
import threading
import time
import traceback
from dataclasses import dataclass, asdict
from enum import Enum
from typing import Any, Callable, Union
import requests
from aiohttp import web
from psplpy.serialization_utils import Serializer


class MpHttpError(Exception):
    def __init__(self, *args, traceback_info: str = ''):
        super().__init__(*args)
        self.traceback_info = traceback_info

    def __str__(self):
        return self.traceback_info

    __repr__ = __str__


class MpHttpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Exception):
            exception_name = type(obj).__name__
            exception_message = str(obj)
            result = f"{exception_name}: {exception_message}"
            return result
        return super().default(obj)


@dataclass
class _SubTask:
    task_id: int
    sub_task_id: int
    data: Any
    result: Any = None


class _TaskResult:
    def __init__(self, task_num: int):
        self.task_num = task_num
        self.finished_task_num = 0
        self.finished_task_list = [None] * task_num  # [None] * 0 = []
        self.is_finished = asyncio.Event()
        self.finished_time = None
        if self.task_num == 0:
            self._set_finished()

    def _set_finished(self):
        self.is_finished.set()
        self.finished_time = time.time()

    def add_finished_subtask(self, sub_task: _SubTask) -> None:
        self.finished_task_list[sub_task.sub_task_id] = sub_task.result
        self.finished_task_num += 1
        if self.finished_task_num == self.task_num:
            self._set_finished()


class MpHttpDataType(Enum):
    JSON = 'j'
    PICKLE = 'p'


@dataclass
class MpKw:
    host: str = '0.0.0.0'
    port: int = 8000
    workers: int = 1
    worker_threads: int = 1
    show_info: bool = True
    max_fetch_timeout: float = 3600
    result_timeout: float = 3600
    recv_types: tuple[MpHttpDataType] = (MpHttpDataType.JSON, MpHttpDataType.PICKLE)


class MpHttpServer(MpKw):
    _POLL_INTERVAL = 0.1

    def __init__(self, kw: MpKw):
        self.__dict__.update(asdict(kw))
        self._check_params()

        self._closed_flag = multiprocessing.Value('b', False)
        self._load = multiprocessing.Value('i', 0)
        self._ahttp_server = _AsyncHttpServer(self)

    def _check_params(self) -> None:
        if self.workers < 1 or self.worker_threads < 1:
            raise ValueError('Number of workers and worker_threads must be 1 or greater than 1')
        self.workers, self.worker_threads = int(self.workers), int(self.worker_threads)

    @staticmethod
    def _get_subtask(func: Callable):
        def wrapper(self, que: multiprocessing.Queue, *args, **kwargs) -> None:
            self.init()
            while True:
                try:
                    sub_task: _SubTask = que.get(timeout=MpHttpServer._POLL_INTERVAL)
                except queue.Empty:
                    if self._closed_flag.value:
                        break
                    continue
                func(self, sub_task, *args, **kwargs)

        return wrapper

    def init(self) -> None:
        ...

    def main_loop(self, data: Any) -> Any:
        return data

    def _main_process(self, req_que: multiprocessing.Queue, result_que: multiprocessing.Queue) -> None:
        @MpHttpServer._get_subtask
        def _process(self, sub_task: Union[multiprocessing.Queue, _SubTask]) -> None:
            with self._load.get_lock():
                self._load.value += 1
            try:
                result = self.main_loop(sub_task.data)
                sub_task.result = result
            except Exception:
                sub_task.result = MpHttpError(traceback_info=traceback.format_exc())
            finally:
                del sub_task.data
                result_que.put(sub_task)
                with self._load.get_lock():
                    self._load.value -= 1

        for _ in range(self.worker_threads):
            threading.Thread(target=_process, args=(self, req_que)).start()

    def run_server(self, new_thread: bool = False) -> 'MpHttpServer':
        for _ in range(self.workers):
            multiprocessing.Process(target=self._main_process, args=(self._ahttp_server._req_que,
                                                                     self._ahttp_server._result_que)).start()
        if self.show_info:
            sys.stderr.write(f"Starting server on ({self.host}, {self.port})...\n")
        if new_thread:
            threading.Thread(target=self._ahttp_server.run).start()
        else:
            self._ahttp_server.run()
        return self

    def close_server(self) -> None:
        self._closed_flag.value = True


class MpHttpPath(Enum):
    SUBMIT = '/submit'
    FETCH = '/fetch'
    LOAD = '/load'
    PROGRESS = '/progress'


class _AsyncHttpServer:
    def __init__(self, s: MpHttpServer):
        self._s = s
        self._serializer = Serializer()
        self._task_id = 0
        self._task_id_lock = asyncio.Lock()
        self._result_dict_lock = asyncio.Lock()
        self._result_dict: dict[int, _TaskResult] = {}
        self._req_que = multiprocessing.Queue()
        self._result_que = multiprocessing.Queue()

        self._app = web.Application()
        self._setup_routes()

    def _setup_routes(self):
        self._app.router.add_post(MpHttpPath.SUBMIT.value, self._handle_submit)
        self._app.router.add_get(MpHttpPath.FETCH.value, self._handle_fetch)
        self._app.router.add_get(MpHttpPath.LOAD.value, self._handle_load)
        self._app.router.add_get(MpHttpPath.PROGRESS.value, self._handle_process)

    async def _put_data(self, data: Any) -> int:
        sub_task_id = 0
        async with self._task_id_lock:
            task_id = self._task_id
            self._task_id += 1
        # create the TaskResult obj first, then put the SubTask, otherwise no obj to store the SubTask result
        async with self._result_dict_lock:
            self._result_dict[task_id] = _TaskResult(len(data))
        for sub_data in data:
            self._req_que.put(_SubTask(task_id, sub_task_id, sub_data))
            sub_task_id += 1
        return task_id

    async def _fetch_result(self, task_id: int, timeout: float, **kwargs) -> list[Any] | TimeoutError | KeyError:
        timeout = timeout if timeout <= self._s.max_fetch_timeout else self._s.max_fetch_timeout
        async with self._result_dict_lock:
            task = self._result_dict.get(task_id)
        if task:
            try:
                await asyncio.wait_for(task.is_finished.wait(), timeout=timeout)
            except asyncio.TimeoutError:
                return TimeoutError(f'Fetch task {task_id} result timeout after {timeout}s')
            else:
                async with self._result_dict_lock:
                    return self._result_dict.pop(task_id).finished_task_list
        return KeyError(f'Task {task_id} result not exist or expired')

    async def _result_distribution(self):
        while True:
            try:
                sub_task: _SubTask = self._result_que.get(block=False)
            except queue.Empty:
                if self._s._closed_flag.value:
                    break
                await asyncio.sleep(self._s._POLL_INTERVAL)
            else:
                async with self._result_dict_lock:
                    self._result_dict[sub_task.task_id].add_finished_subtask(sub_task)

    async def _cleanup_expired_results(self):
        last_cleanup_time = time.time()
        while True:
            if time.time() - last_cleanup_time > self._s.result_timeout / 10:
                expired_task_ids = []
                for task_id, task in self._result_dict.items():
                    if task.is_finished.is_set() and time.time() - task.finished_time > self._s.result_timeout:
                        expired_task_ids.append(task_id)
                async with self._result_dict_lock:
                    for task_id in expired_task_ids:
                        self._result_dict.pop(task_id)
                if self._s.show_info and expired_task_ids:
                    time_str = datetime.datetime.now().strftime("[%d/%b/%Y %H:%M:%S]")
                    sys.stderr.write(f'Warning - {time_str} - Result of tasks {expired_task_ids} has expired\n')
                last_cleanup_time = time.time()
            else:
                if self._s._closed_flag.value:
                    break
                await asyncio.sleep(self._s._POLL_INTERVAL)

    @staticmethod
    def _exception_handler(func):
        @functools.wraps(func)
        async def wrapper(self, request: web.Request):
            try:
                response = await func(self, request)
            except Exception:
                traceback.print_exc()
                response = web.Response(text='Internal Server Error', status=500)
            if self._s.show_info:
                current_time = datetime.datetime.now().strftime('%d/%b/%Y %H:%M:%S.%f')
                log_message = (f'-{request.remote}- [{current_time}] {request.method} {request.path} '
                               f'{request.content_length} {response.status} {len(response.body)} \n')
                sys.stderr.write(log_message)
            return response

        return wrapper

    def _return_by_data_type(self, result: Any, data_type: str, status: int = 200) -> web.Response:
        if data_type == MpHttpDataType.PICKLE.value:
            return web.Response(body=self._serializer.dump_pickle(result), status=status,
                                content_type='application/octet-stream')
        else:
            return web.Response(text=json.dumps(result, cls=MpHttpEncoder), status=status,
                                content_type='application/json')

    @_exception_handler
    async def _handle_submit(self, request: web.Request):
        content_type = request.content_type
        data_type = MpHttpDataType.JSON.value
        if content_type == 'application/octet-stream':
            data_type = MpHttpDataType.PICKLE.value

        if content_type == 'application/json' and MpHttpDataType.JSON in self._s.recv_types:
            data: Any | list[Any] = await request.json()
            if not isinstance(data, list):
                data = [data]
        elif content_type == 'application/octet-stream' and MpHttpDataType.PICKLE in self._s.recv_types:
            data: bytes = await request.read()
            data: Any = self._serializer.load_pickle(data)
        else:
            return self._return_by_data_type(ValueError("Unsupported Content-Type"), data_type, 415)
        task_id = await self._put_data(data)
        return self._return_by_data_type(task_id, data_type)

    def _process_params(self, request: web.Request, required_params: tuple = ('task_id')
                        ) -> tuple[dict | None, web.Response | None]:
        params = dict(request.query)
        if not params.get('data_type'):
            params['data_type'] = MpHttpDataType.JSON.value

        if 'task_id' in required_params:
            if params.get('task_id') is None:
                err_info = "Missing required parameter: 'id'"
                return None, self._return_by_data_type(ValueError(err_info), params['data_type'], 400)
            else:
                try:
                    params['task_id'] = int(params['task_id'])
                except ValueError:
                    err_info = "Invalid parameter type for 'task_id'. Expected an integer."
                    return None, self._return_by_data_type(ValueError(err_info), params['data_type'], 400)
        if params.get('timeout'):
            try:
                params['timeout'] = float(params['timeout'])
            except ValueError:
                err_info = "Invalid parameter type for 'timeout'. Expected a float."
                return None, self._return_by_data_type(ValueError(err_info), params['data_type'], 400)
        else:
            params['timeout'] = self._s.max_fetch_timeout
        return params, None

    @_exception_handler
    async def _handle_fetch(self, request: web.Request):
        params, response = self._process_params(request)
        if response:
            return response
        result = await self._fetch_result(**params)
        return self._return_by_data_type(result, params['data_type'])

    @_exception_handler
    async def _handle_load(self, request: web.Request):
        params, response = self._process_params(request, required_params=())
        load = self._s._load.value / (self._s.workers * self._s.worker_threads)
        return self._return_by_data_type(load, params['data_type'])

    @_exception_handler
    async def _handle_process(self, request: web.Request):
        params, response = self._process_params(request)
        if response:
            return response
        async with self._result_dict_lock:
            task = self._result_dict.get(params['task_id'])
        if task is None:
            return self._return_by_data_type(ValueError(f"No task with task_id '{params['task_id']}'"),
                                             params['data_type'], 404)
        return self._return_by_data_type((task.finished_task_num, task.task_num), params['data_type'])

    async def _start_server(self):
        runner = web.AppRunner(self._app)
        await runner.setup()
        site = web.TCPSite(runner, self._s.host, self._s.port)
        await site.start()

        task_distribution = asyncio.create_task(self._result_distribution())
        task_clean = asyncio.create_task(self._cleanup_expired_results())
        await task_distribution
        await task_clean

        await runner.cleanup()
        if self._s.show_info:
            sys.stderr.write(f'Server on ({self._s.host}, {self._s.port}) stopped.\n')

    def run(self):
        asyncio.run(self._start_server())


class MpHttpClient:
    def __init__(self, host: str = '127.0.0.1', port: int = 8080, server: MpHttpServer = None):
        self.host, self.port = host, port
        if server:
            self.host, self.port = server.host if server.host != '0.0.0.0' else '127.0.0.1', server.port

        self._loader = Serializer().load_pickle
        self._dumper = Serializer().dump_pickle
        self._data_type = MpHttpDataType.PICKLE.value
        self._headers = {'Content-Type': 'application/octet-stream'}

    def _resp(self, resp: requests.Response) -> Any:
        if resp.status_code != 200:
            raise ValueError(f"Request failed with status '{resp.status_code}', message: '{resp.text}'")
        return self._loader(resp.content)

    def _post(self, data: Any, path: str) -> Any:
        dumped_data = self._dumper(data)
        resp = requests.post(f'http://{self.host}:{self.port}{path}', data=dumped_data, headers=self._headers)
        return self._resp(resp)

    def _get(self, params: dict, path: str) -> Any:
        params['data_type'] = self._data_type
        resp = requests.get(f'http://{self.host}:{self.port}{path}', params=params, headers=self._headers)
        return self._resp(resp)

    def submit(self, data_list: list | tuple) -> int:
        """Getting the task_id for fetching data from the server"""
        return self._post(data_list, MpHttpPath.SUBMIT.value)

    def fetch(self, task_id: int, timeout: float = 3600) -> list[Any]:
        """The max timeout time depends on the setting of the server"""
        result = self._get({'task_id': task_id, 'timeout': timeout}, MpHttpPath.FETCH.value)
        if isinstance(result, (TimeoutError, KeyError)):
            raise result
        return result

    def batch(self, data_list: list | tuple, timeout: float = 3600) -> list[Any]:
        return self.fetch(self.submit(data_list), timeout)

    def get(self, data: Any, timeout: float = 3600) -> Any:
        return self.batch([data], timeout)[0]

    def load(self) -> float:
        return self._get({}, MpHttpPath.LOAD.value)

    def progress(self, task_id: int) -> tuple[int, int]:
        """return the tuple (finished_task_num, total_task_num)"""
        return tuple(self._get({'task_id': task_id}, MpHttpPath.PROGRESS.value))


class MpHttpClientJson(MpHttpClient):
    def __init__(self, host: str = '127.0.0.1', port: int = 8080, server: MpHttpServer = None):
        super().__init__(host, port, server)

        self._loader = json.loads
        self._dumper = json.dumps
        self._data_type = MpHttpDataType.JSON.value
        self._headers = {'Content-Type': 'application/json'}
