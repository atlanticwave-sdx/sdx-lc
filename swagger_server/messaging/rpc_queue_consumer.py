#!/usr/bin/env python
import logging
import os
import threading
from queue import Queue

import pika

MQ_HOST = os.environ.get("MQ_HOST")
MQ_PORT = os.environ.get("MQ_PORT")
MQ_USER = os.environ.get("MQ_USER")
MQ_PASS = os.environ.get("MQ_PASS")

# subscribe to the corresponding queue
SUB_QUEUE = os.environ.get("SUB_QUEUE")
SUB_TOPIC = os.environ.get("SUB_TOPIC")
SUB_EXCHANGE = os.environ.get("SUB_EXCHANGE")

SUB_QUEUE = "connection"
SUB_TOPIC = "lc1_q1"
SUB_EXCHANGE = "connection"


class RpcConsumer(object):
    def __init__(self, thread_queue, exchange_name):
        self.logger = logging.getLogger(__name__)
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=MQ_HOST,
                port=MQ_PORT,
                credentials=pika.PlainCredentials(username=MQ_USER, password=MQ_PASS),
            )
        )

        self.channel = self.connection.channel()
        self.exchange_name = exchange_name

        # self.result = self.channel.queue_declare(queue=SUB_QUEUE)
        self.result = self.channel.queue_declare(queue="")
        self._thread_queue = thread_queue

        self.binding_keys = []
        self.binding_keys.append(SUB_TOPIC)

        # self.channel.exchange_declare(exchange=SUB_TOPIC, exchange_type='topic')
        # self.channel.queue_bind(exchange=SUB_TOPIC, queue=SUB_QUEUE, routing_key=SUB_TOPIC)

    def on_request(self, ch, method, props, message_body):
        response = message_body
        self._thread_queue.put(message_body)

        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=MQ_HOST,
                port=MQ_PORT,
                credentials=pika.PlainCredentials(username=MQ_USER, password=MQ_PASS),
            )
        )
        self.channel = self.connection.channel()

        ch.basic_publish(
            exchange=self.exchange_name,
            routing_key=props.reply_to,
            properties=pika.BasicProperties(correlation_id=props.correlation_id),
            body=str(response),
        )
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def start_consumer(self):
        # self.channel.queue_declare(queue=SUB_QUEUE)
        self.channel.exchange_declare(exchange=SUB_EXCHANGE, exchange_type="topic")
        queue_name = self.result.method.queue
        print("queue_name: " + queue_name)

        # binding to: queue--'', exchange--connection, routing_key--lc1_q1
        for binding_key in self.binding_keys:
            self.channel.queue_bind(
                exchange=SUB_EXCHANGE, queue=queue_name, routing_key=binding_key
            )

        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue=SUB_QUEUE, on_message_callback=self.on_request)

        self.logger.info(" [MQ] Awaiting requests from queue: " + SUB_QUEUE)
        self.channel.start_consuming()


if __name__ == "__main__":
    thread_queue = Queue()
    rpc = RpcConsumer(thread_queue, "connection")

    t1 = threading.Thread(target=rpc.start_consumer, args=())
    t1.start()

    while True:
        if not thread_queue.empty():
            print("-----thread-----got message: " + str(thread_queue.get()))
            print("----------")
    # rpc.start_consumer()

#!/usr/bin/env python
# import pika

# def on_request(ch, method, props, body):
#     response = body

#     ch.basic_publish(exchange='',
#                      routing_key=props.reply_to,
#                      properties=pika.BasicProperties(correlation_id = \
#                                                          props.correlation_id),
#                      body=str(response))
#     ch.basic_ack(delivery_tag=method.delivery_tag)

# if __name__ == "__main__":
#     connection = pika.BlockingConnection(pika.ConnectionParameters(host='aw-sdx-monitor.renci.org'))

#     channel = connection.channel()

#     channel.queue_declare(queue='rpc_queue')

#     channel.basic_qos(prefetch_count=1)
#     channel.basic_consume(queue='rpc_queue', on_message_callback=on_request)

#     print("Awaiting RPC requests")
#     channel.start_consuming()
