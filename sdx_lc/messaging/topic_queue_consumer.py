#!/usr/bin/env python
import logging
import os
import threading
from queue import Queue

import pika

from sdx_lc.handlers.sdx_controller_msg_handler import SdxControllerMsgHandler
from sdx_datamodel.constants import MessageQueueNames

MQ_HOST = os.environ.get("MQ_HOST")
MQ_PORT = os.environ.get("MQ_PORT")
MQ_USER = os.environ.get("MQ_USER")
MQ_PASS = os.environ.get("MQ_PASS")


class TopicQueueConsumer(object):
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

        self.result = self.channel.queue_declare(queue="", exclusive=True)
        self._thread_queue = thread_queue

        self.routing_key = os.getenv("SDXLC_DOMAIN")
        self.sdx_controller_msg_handler = SdxControllerMsgHandler()

    def on_rpc_request(self, ch, method, props, message_body):
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

    def callback(self, ch, method, properties, body):
        self.sdx_controller_msg_handler.process_sdx_controller_json_msg(body)

    def start_consumer(self):
        # self.channel.queue_declare(queue=SUB_QUEUE)
        self.channel.exchange_declare(
            exchange=self.exchange_name, exchange_type="topic"
        )
        queue_name = self.result.method.queue

        self.channel.queue_bind(
            exchange=self.exchange_name, queue=queue_name, routing_key=self.routing_key
        )

        self.channel.basic_qos(prefetch_count=1)

        self.channel.basic_consume(
            queue=queue_name, on_message_callback=self.callback, auto_ack=True
        )

        self.logger.info(
            f" [MQ] Awaiting requests from queue:'{queue_name}'"
            f" with exchange_name: '{self.exchange_name}'"
            f" routing_key:'{self.routing_key}'"
            f" (MQ_HOST: {MQ_HOST}, MQ_PORT: {MQ_PORT})"
        )

        self.channel.start_consuming()


if __name__ == "__main__":
    SUB_QUEUE = MessageQueueNames.CONNECTIONS
    thread_queue = Queue()
    consumer = TopicQueueConsumer(thread_queue, SUB_QUEUE)

    t1 = threading.Thread(target=consumer.start_consumer, args=())
    t1.start()

    while True:
        if not thread_queue.empty():
            print("-----thread-----got message: " + str(thread_queue.get()))
            print("----------")
