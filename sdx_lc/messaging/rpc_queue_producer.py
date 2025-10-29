#!/usr/bin/env python
import json
import logging
import os
import threading
import time
import uuid

import pika

MQ_HOST = os.environ.get("MQ_HOST")
MQ_PORT = os.environ.get("MQ_PORT")
MQ_USER = os.environ.get("MQ_USER")
MQ_PASS = os.environ.get("MQ_PASS")
SDXLC_DOMAIN = os.environ.get("SDXLC_DOMAIN")
HEARTBEAT_INTERVAL = int(os.getenv("HEARTBEAT_INTERVAL", 30))  # seconds


class RpcProducer(object):
    def __init__(self, timeout, exchange_name, routing_key):
        self.logger = logging.getLogger(__name__)
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=MQ_HOST,
                port=MQ_PORT,
                credentials=pika.PlainCredentials(username=MQ_USER, password=MQ_PASS),
            )
        )

        self.channel = self.connection.channel()
        self.timeout = timeout
        self.exchange_name = exchange_name
        self.routing_key = routing_key

        self.stop_keep_live = False

        t1 = threading.Thread(target=self.keep_live, args=())
        t1.start()

        # set up callback queue
        result = self.channel.queue_declare(queue="", exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True,
        )

    def stop(self):
        """
        Signal to stop keep-alive pings, so that RpcProducer instances
        can be safely deleted.
        """
        self.stop_keep_live = True

    def keep_live(self):
        while self.stop_keep_live != True:
            time.sleep(HEARTBEAT_INTERVAL)
            msg = {"type": "Heart Beat", "domain": SDXLC_DOMAIN}
            self.logger.debug("Sending heart beat msg.")
            self.call(json.dumps(msg))

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, body):
        # if not self.connection or self.connection.is_closed:
        #     # print("Reopening connection...")
        #     self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=MQ_HOST))
        #     self.channel = self.connection.channel()
        #     # print("Connection reopened.")
        #     # channel.exchange_declare(exchange=self.exchange_name)

        self.response = None
        self.corr_id = str(uuid.uuid4())

        self.channel.basic_publish(
            exchange=self.exchange_name,
            routing_key=self.routing_key,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=str(body),
        )

        timer = 0
        while self.response is None:
            time.sleep(1)
            timer += 1
            if timer == self.timeout:
                return "No response from MQ receiver"
            self.connection.process_data_events()

        # self.channel.close()
        return self.response


if __name__ == "__main__":
    rpc = RpcProducer(timeout=1, exchange_name="", routing_key=str(uuid.uuid4()))
    body = "test body"
    print("Published Message: {}".format(body))
    response = rpc.call(body)
    print(" [.] Got response: " + str(response))
    rpc.stop()
