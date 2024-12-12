from concurrent import futures

from tests.__init__ import *
from psplpy.network_utils import *


def get_ip_address():
    try:
        temp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        temp_socket.connect(("114.114.114.114", 80))  # connect to a public ip address
        ip_address = temp_socket.getsockname()[0]  # get the host's ip
        temp_socket.close()
        return ip_address
    except socket.error:
        return None


port = 12345
host_ip = get_ip_address()
client_port = find_free_port(host_ip, try_range=(12345, 12999))
data = b"Hello World" * 1024 * 32


def sender():
    def handler(client_socket: ClientSocket, addr):
        print(f'client {addr}')
        assert addr == (host_ip, client_port)

        received_data = client_socket.recv()
        assert received_data == data
        client_socket.send(data)
        recv_tmp_file = tmp_dir / 'recv_tmp.tmp'
        client_socket.recvf(recv_tmp_file)
        assert tmp_file.read_text() == recv_tmp_file.read_text()

        tmp_file.unlink()
        recv_tmp_file.unlink()
        client_socket.close()
        server.close()

    server = ServerSocket(port=port)
    server.handle(handler)


def recver():
    client = ClientSocket(port=port, client_host=host_ip, client_port=client_port)
    client.connect()
    client.send(data)
    received_data = client.recv()
    assert received_data == data
    tmp_file.write_bytes(data)
    client.sendf(tmp_file)
    client.close()


def test_find():
    def handler(client_socket: ClientSocket, addr):
        client_socket.close()

    test_port = find_free_port(host_ip, [12345, ], [12346, ], (12345, 12999))
    print(f'test port {test_port}')
    s = ServerSocket(host=host_ip, port=test_port)
    s.handle(handler)
    assert find_running_port(host=host_ip, try_range=(test_port - 100, test_port + 100)) == test_port
    assert find_running_port(host=host_ip, try_ports=[test_port, ], exclude_ports=[test_port, ],
                             try_range=(test_port - 100, test_port + 100)) is None

    s.close()


def tests():
    with futures.ThreadPoolExecutor() as executor:
        sender_future = executor.submit(sender)
        time.sleep(0.1)
        recver_future = executor.submit(recver)
        time.sleep(0.1)
        sender_future.result(), recver_future.result()
    test_find()


if __name__ == '__main__':
    tests()
