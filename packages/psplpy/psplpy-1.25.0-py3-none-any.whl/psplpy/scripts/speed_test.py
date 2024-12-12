import time
from typing import Any
from psplpy.network_utils import ServerSocket, ClientSocket
from psplpy.other_utils import overlay_print


class SpeedTestServer:
    def __init__(self, server_socket: ServerSocket):
        self.server_socket = server_socket

    @staticmethod
    def handler(client_socket: ClientSocket, addr: Any):
        print(f'Connection from {addr}')
        t_start = time.time()
        total_length = 0
        while True:
            this_t_start = time.time()
            data = client_socket.recv()
            if not data:
                break
            total_length += len(data)
            total_mb = total_length / (1024 * 1024)
            speed = total_mb / (time.time() - t_start)
            current_speed = (len(data) / (1024 * 1024)) / (time.time() - this_t_start)
            overlay_print(f'Received: {total_mb:.2f} mb, avg speed {speed:.2f} mb/s, '
                          f'current speed {current_speed:.2f} mb/s')
        print(f'\nConnection from {addr} closed')

    def start(self):
        print(f'Starting server on ({self.server_socket.host}, {self.server_socket.port})')
        self.server_socket.handle(self.handler)


class SpeedTestClient:
    def __init__(self, client_socket: ClientSocket, data_size_mb: float = 1):
        self.client_socket = client_socket
        self.test_data = b'10' * int(512 * 1024 * data_size_mb)

    def start(self, test_seconds: float = 30):
        self.client_socket.connect()
        total_length = 0
        t_start = time.time()
        while time.time() - t_start < test_seconds:
            self.client_socket.send(self.test_data)
            total_length += len(self.test_data)
            total_mb = total_length / (1024 * 1024)
            overlay_print(f'Sent {total_mb} mb')
        print('Test finished')


if __name__ == '__main__':
    SpeedTestServer(ServerSocket()).start()
