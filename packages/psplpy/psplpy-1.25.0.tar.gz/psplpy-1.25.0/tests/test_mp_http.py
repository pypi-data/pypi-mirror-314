from tests.__init__ import *
import aiohttp
from concurrent import futures
from psplpy.network_utils import find_free_port
from psplpy.other_utils import PerfCounter
from psplpy.mp_http import *


def test_lots_of_short_tasks():
    # lots of short tasks test
    s = MpHttpServer(MpKw(workers=2, worker_threads=1, port=find_free_port())).run_server(new_thread=True)
    time.sleep(0.25)
    c = MpHttpClient(server=s)
    task_id = c.submit(['1'] * 10000)
    p = PerfCounter()
    result = c.fetch(task_id)
    p.show()
    s.close_server()


def test_high_concurrency():
    class TestServer(MpHttpServer):
        def init(self) -> None:
            self.num = 1

        def main_loop(self, data: Any) -> Any:
            data = data['data']
            time.sleep(data)
            return {'result': data, 'num': self.num}

    s = TestServer(MpKw(port=find_free_port(), workers=8, worker_threads=100,
                        max_fetch_timeout=100, result_timeout=100)).run_server(new_thread=True)
    time.sleep(0.5)

    async def fetch_get(session, url, params=None):
        async with session.get(url, params=params) as response:
            return await response.text()

    async def fetch_post(session: aiohttp.ClientSession, url, data=None):
        async with session.post(url, json=data) as response:
            return await response.text()

    async def run_client(reqs):
        async with aiohttp.ClientSession() as session:
            tasks = []
            count = 0
            for url, params in reqs:
                if MpHttpPath.SUBMIT.value in url:
                    tasks.append(fetch_post(session, url, params))
                else:
                    tasks.append(fetch_get(session, url, params))
                count += 1
                if count == num:
                    time.sleep(0.1)
            responses = await asyncio.gather(*tasks)
            return responses

    num = 1000
    url = f'http://127.0.0.1:{s.port}'
    reqs = [(f'{url}{MpHttpPath.SUBMIT.value}', {'data': 2})] * num
    for i in range(num):
        reqs.append((f'{url}{MpHttpPath.FETCH.value}', {'task_id': i}))
    for i in range(num):
        reqs.append((f'{url}{MpHttpPath.LOAD.value}', None))
    for i in range(num):
        reqs.append((f'{url}{MpHttpPath.PROGRESS.value}', {'task_id': i}))

    start_time = time.time()
    responses = asyncio.run(run_client(reqs))
    end_time = time.time()
    print(responses)
    print(f'Total requests: {len(reqs)}')
    print(f'Time taken: {end_time - start_time:.2f} seconds')
    s.close_server()


def test_mp_http():
    class TestServer(MpHttpServer):
        def init(self) -> None:
            self.num = 1

        def main_loop(self, data: Any) -> Any:
            time.sleep(data)
            return {'result': data, 'num': self.num}

    def show_load(c: MpHttpClient):
        time.sleep(0.25)
        return c.load()

    s = TestServer(MpKw(port=find_free_port(), workers=6, max_fetch_timeout=2,
                        result_timeout=1)).run_server(new_thread=True)
    time.sleep(0.25)
    c = MpHttpClient(server=s)

    # test get load and batch
    load_results = futures.ThreadPoolExecutor().map(show_load, [c])  # starting a new thread to get the load
    print(1, datetime.datetime.now().strftime('%d/%b/%Y %H:%M:%S.%f'))
    result = c.batch([0.5, 0.75, 1])
    load_results = list(load_results)
    assert load_results == [0.5], load_results
    assert result == [{'result': 0.5, 'num': 1}, {'result': 0.75, 'num': 1}, {'result': 1, 'num': 1}], result

    # test get progress
    data_list = [0.5, 0.75, 1]
    task_id = c.submit(data_list)
    assert isinstance(task_id, int)
    task_progress = c.progress(task_id)
    assert task_progress == (0, len(data_list)), task_progress
    time.sleep(0.75 + 0.05)
    task_progress = c.progress(task_id)
    assert task_progress == (2, len(data_list)), task_progress
    time.sleep(1 - 0.75)

    # test task result expiration and task fetch timeout
    time.sleep(2)
    try:
        result = c.fetch(task_id)
    except KeyError as e:
        print(e)
    else:
        assert False
    task_id = c.submit([3])
    try:
        result = c.fetch(task_id)
    except TimeoutError as e:
        print(e)
    else:
        assert False
    time.sleep(1.5)

    # test no load
    assert c.load() == 0
    time.sleep(0.25)

    # test send empty list
    task_id = c.submit([])
    assert c.fetch(task_id) == []

    s.close_server()


def test_json():
    class TestServer(MpHttpServer):
        def init(self) -> None:
            self.num = 1

        def main_loop(self, data: Any) -> Any:
            return {'result': data, 'num': self.num}

    s = TestServer(MpKw(port=find_free_port(), workers=2)).run_server(new_thread=True)
    time.sleep(0.25)
    c = MpHttpClientJson(server=s)

    task_id = c.submit(data_list=[{'a': (1,)}, ])
    assert task_id == 0
    assert c.progress(task_id) == (0, 1)
    assert c.fetch(task_id) == [{'result': {'a': [1]}, 'num': 1}]
    assert c.load() == 0

    s.close_server()


def tests():
    test_high_concurrency()
    test_mp_http()
    test_lots_of_short_tasks()
    test_json()


if __name__ == '__main__':
    tests()
