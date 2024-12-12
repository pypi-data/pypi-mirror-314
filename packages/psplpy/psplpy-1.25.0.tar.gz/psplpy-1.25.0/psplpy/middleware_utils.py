import threading
from typing import Any, Callable
import pika
import requests
from requests.auth import HTTPBasicAuth
from psplpy.serialization_utils import Serializer, CompressSerializer


class _RabbitmqManagement:
    def __init__(self, host: str, management_port: int, user: str, pw: str):
        self.api_url = f'http://{host}:{management_port}/api'
        self.auth = HTTPBasicAuth(user, pw)

    def _vhost(self, vhost_name: str, method: str) -> str:
        url = f'{self.api_url}/vhosts/{vhost_name}'
        response = getattr(requests, method)(url, auth=self.auth)
        if response.status_code not in [201, 204]:
            raise AssertionError(f'Failed to {method} vhost: {vhost_name}, status code: {response.status_code}')
        return vhost_name

    def create_vhost(self, vhost_name: str) -> str:
        return self._vhost(vhost_name, 'put')

    def delete_vhost(self, vhost_name: str) -> str:
        return self._vhost(vhost_name, 'delete')

    def list_vhosts(self) -> list[str]:
        url = f'{self.api_url}/vhosts'
        response = requests.get(url, auth=self.auth)
        if response.status_code == 200:
            vhosts = response.json()
            return [vhost['name'] for vhost in vhosts]
        raise AssertionError(f'Failed to list vhosts, status code: {response.status_code}')


class Rabbitmq:
    HOST = 'localhost'
    PORT = 5672
    MANAGEMENT_PORT = 15672
    USER = 'guest'
    PW = 'guest'
    VIRTUAL_HOST = '/'

    JSON = 'j'
    PICKLE = 'p'
    AUTO = CompressSerializer.AUTO

    def __init__(self, host: str = None, port: int = None, user: str = None, pw: str = None, virtual_host: str = None,
                 management_port: int = None, serializer: str = PICKLE, compress: bool | str = False,
                 compress_threshold: int = 1024 * 128, **kwargs):
        self.host = host or self.HOST
        self.port = port or self.PORT
        self.user = user or self.USER
        self.pw = pw or self.PW
        self.virtual_host = virtual_host or self.VIRTUAL_HOST
        self.management_port = management_port or self.MANAGEMENT_PORT
        self.serializer, self.compress, self.compress_threshold = serializer, compress, compress_threshold
        self._serializer = CompressSerializer(compress=self.compress, threshold=self.compress_threshold)
        self.management = _RabbitmqManagement(self.host, self.management_port, self.user, self.pw)

        credentials = pika.PlainCredentials(self.user, self.pw)
        parameters = pika.ConnectionParameters(self.host, self.port, self.virtual_host, credentials, **kwargs)
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()

        self._stop_consuming = False
        self._suppress_error = False

    def _serialize(self, data: Any) -> bytes:
        if self.serializer == self.PICKLE:
            return self.PICKLE.encode() + self._serializer.dump_pickle(data)
        else:
            raise ValueError(f'Unsupported serializer: {self.serializer}')

    def _deserialize(self, data: bytes) -> Any:
        serializer = chr(data[0])
        data = data[1:]
        if serializer == self.PICKLE:
            return self._serializer.load_pickle(data)
        else:
            raise ValueError(f'Unsupported serializer: {self.serializer}')

    @staticmethod
    def _default_callback(ch, method, properties, body) -> None:
        print(body)

    def _callback(self, ch, method, properties, body) -> None:
        body = self._deserialize(body)
        self.callback(ch, method, properties, body)
        if self._stop_consuming:
            ch.stop_consuming()

    def send_init(self, exchange: str, routing_keys: list[str]) -> None:
        self.exchange = exchange
        self.routing_keys = routing_keys
        self.channel.exchange_declare(exchange=self.exchange, exchange_type='topic')

    def recv_init(self, exchange: str, binding_keys: list[str], callback: Callable = None) -> None:
        self.send_init(exchange, routing_keys=binding_keys)
        self.callback = callback or self._default_callback
        queue = self.channel.queue_declare('', exclusive=True)
        self.queue_name = queue.method.queue
        for routing_key in self.routing_keys:
            self.channel.queue_bind(exchange=self.exchange, queue=self.queue_name, routing_key=routing_key)
        self.channel.basic_consume(queue=self.queue_name, on_message_callback=self._callback, auto_ack=True)

    def basic_publish(self, body: Any) -> None:
        for routing_key in self.routing_keys:
            self.channel.basic_publish(exchange=self.exchange, routing_key=routing_key, body=self._serialize(body))

    def _start_consuming(self) -> None:
        try:
            self.channel.start_consuming()
        except Exception as e:
            if not self._suppress_error:
                raise e

    def start_consuming(self) -> threading.Thread:
        t = threading.Thread(target=self._start_consuming)
        t.start()
        return t

    def stop_consuming(self):
        self._stop_consuming = True

    def close(self, suppress_error: bool = False) -> None:
        self._suppress_error = suppress_error
        try:
            self.connection.close()
        except Exception as e:
            if not self._suppress_error:
                raise e
