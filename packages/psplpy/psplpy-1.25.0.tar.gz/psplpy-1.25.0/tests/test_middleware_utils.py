from tests.__init__ import *
from psplpy.middleware_utils import Rabbitmq


Rabbitmq.HOST = get_env('RABBITMQ_HOST')
Rabbitmq.USER = get_env('RABBITMQ_USER')
Rabbitmq.PW = get_env('RABBITMQ_PW')

send_data1 = {'1': 100, '2': False, '3': '你好', '4': 3.14}
send_data2 = {'1': -1, '2': True, '3': 'hello', '4': 2/3}
receiver1_data_list, receiver2_data_list, receiver3_data_list = [], [], []


def callback1(ch, method, properties, body) -> None:
    global receiver1_data_list
    receiver1_data_list.append(body)
    print(body)


def callback2(ch, method, properties, body) -> None:
    global receiver2_data_list
    receiver2_data_list.append(body)
    print(body)


def callback3(ch, method, properties, body) -> None:
    global receiver3_data_list
    receiver3_data_list.append(body)
    print(body)


def tests():
    exchange = 'test'

    rabbitmq_receiver1 = Rabbitmq(serializer=Rabbitmq.JSON, compress=True)
    rabbitmq_receiver1.recv_init(exchange=exchange, binding_keys=['rabbit.*.quickly', 'direct'], callback=callback1)
    rabbitmq_receiver1.start_consuming()

    rabbitmq_receiver1.management.create_vhost('test')
    print(rabbitmq_receiver1.management.list_vhosts())
    assert rabbitmq_receiver1.management.list_vhosts() == ['/', 'test']
    rabbitmq_receiver1.management.delete_vhost('test')
    assert rabbitmq_receiver1.management.list_vhosts() == ['/']

    rabbitmq_receiver2 = Rabbitmq(serializer=Rabbitmq.PICKLE, compress=True)
    # will receive all routing keys' messages like fanout
    rabbitmq_receiver2.recv_init(exchange=exchange, binding_keys=['#'], callback=callback2)
    rabbitmq_receiver2.start_consuming()

    rabbitmq_receiver3 = Rabbitmq(serializer=Rabbitmq.PICKLE, compress=True)
    rabbitmq_receiver3.recv_init(exchange=exchange, binding_keys=['*.jump.*', '#.critical'], callback=callback3)
    rabbitmq_receiver3.start_consuming()

    rabbitmq_sender1 = Rabbitmq(serializer=Rabbitmq.PICKLE, compress=True)
    rabbitmq_sender1.send_init(exchange=exchange, routing_keys=['rabbit.jump.quickly', 'direct'])
    rabbitmq_sender1.basic_publish(send_data1)

    rabbitmq_sender2 = Rabbitmq(serializer=Rabbitmq.PICKLE, compress=True)
    rabbitmq_sender2.send_init(exchange=exchange, routing_keys=['node1.kern.critical', 'direct'])
    rabbitmq_sender2.basic_publish(send_data2)

    # if it fails, increasing the interval
    time.sleep(0.5)
    rabbitmq_receiver1.stop_consuming()
    rabbitmq_receiver1.close(suppress_error=True)
    rabbitmq_receiver2.close(suppress_error=True)
    rabbitmq_receiver3.close(suppress_error=True)

    global receiver1_data_list, receiver2_data_list, receiver3_data_list
    assert (sorted(receiver1_data_list, key=lambda x: x['1']) ==
            sorted([send_data1] * 2 + [send_data2], key=lambda x: x['1'])), receiver1_data_list
    assert (sorted(receiver2_data_list, key=lambda x: x['1']) ==
            sorted([send_data1] * 2 + [send_data2] * 2, key=lambda x: x['1'])), receiver2_data_list
    assert (sorted(receiver3_data_list, key=lambda x: x['1']) ==
            sorted([send_data1] + [send_data2], key=lambda x: x['1'])), receiver3_data_list

    rabbitmq_sender1.channel.exchange_delete(exchange=exchange)
    rabbitmq_sender1.close()
    rabbitmq_sender2.close()


if __name__ == '__main__':
    tests()
