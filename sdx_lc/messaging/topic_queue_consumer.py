#!/usr/bin/env python
import json
import logging
import os
import threading
from queue import Queue

import pika
import requests

from sdx_lc.utils.db_utils import DbUtils

MQ_HOST = os.environ.get("MQ_HOST")
MQ_PORT = os.environ.get("MQ_PORT")
MQ_USER = os.environ.get("MQ_USER")
MQ_PASS = os.environ.get("MQ_PASS")

OXPO_USER = os.environ.get("OXPO_USER", None)
OXPO_PASS = os.environ.get("OXPO_PASS", None)
OXP_CONNECTION_URL = os.environ.get("OXP_CONNECTION_URL")


def is_json(myjson):
    try:
        json.loads(myjson)
    except ValueError as e:
        return False
    return True


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

        # Get DB connection and tables set up.
        self.db_instance = DbUtils()
        self.db_instance.initialize_db()

        self.heartbeat_id = 0
        self.message_id = 0

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
        # if 'Heart Beat' not in str(body):
        #     print(" [x] %r:%r" % (method.routing_key, body))
        self.handle_mq_msg(body)

    def handle_mq_msg(self, msg_body):
        if "Heart Beat" in str(msg_body):
            self.heartbeat_id += 1
            self.logger.debug("Heart beat received. ID: " + str(self.heartbeat_id))
            return

        self.logger.info("MQ received message:" + str(msg_body))

        if is_json(msg_body):
            self.logger.info("JSON message")
            msg_json = json.loads(msg_body)
            if (
                "link" in msg_json
                and "uni_a" in msg_json["link"]
                and "uni_z" in msg_json["link"]
            ):
                connection = msg_json["link"]
                self.logger.info("Got connection message.")
                self.db_instance.add_key_value_pair_to_db(self.message_id, connection)
                self.logger.info("Save to database complete.")
                self.logger.info("Message ID:" + str(self.message_id))
                self.message_id += 1
                self.logger.info("Sending connection info to OXP.")
                # send connection info to OXP
                if msg_json.get("operation") == "post":
                    try:
                        r = requests.post(
                            str(OXP_CONNECTION_URL),
                            json=connection,
                            auth=(OXPO_USER, OXPO_PASS),
                        )
                        self.logger.info(f"Status from OXP: {r}")
                    except Exception as e:
                        self.logger.error(f"Error on POST to {OXP_CONNECTION_URL}: {e}")
                        self.logger.info(
                            "Check your configuration and make sure OXP service is running."
                        )
                elif msg_json.get("operation") == "delete":
                    try:
                        r = requests.delete(
                            str(OXP_CONNECTION_URL),
                            json=connection,
                            auth=(OXPO_USER, OXPO_PASS),
                        )
                        self.logger.info(f"Status from OXP: {r}")
                    except Exception as e:
                        self.logger.error(f"Error on DELETE {OXP_CONNECTION_URL}: {e}")
                        self.logger.info(
                            "Check your configuration and make sure OXP service is running."
                        )
            elif "version" in msg_json:
                msg_id = msg_json["id"]
                lc_name = msg_json["name"]
                msg_version = msg_json["version"]
                db_msg_id = str(lc_name) + "-" + str(msg_id) + "-" + str(msg_version)
                self.db_instance.add_key_value_pair_to_db(db_msg_id, msg_body)
                self.logger.info("Save to database complete.")
                self.logger.info("message ID:" + str(db_msg_id))
            else:
                self.logger.info("Got message: " + str(msg_body))
        else:
            self.logger.info("Other type of message")
            self.db_instance.add_key_value_pair_to_db(self.message_id, msg_body)
            self.logger.info("Save to database complete.")
            self.logger.info("Message ID:" + str(self.message_id))
            self.message_id += 1

    def start_consumer(self):
        # self.channel.queue_declare(queue=SUB_QUEUE)
        self.channel.exchange_declare(
            exchange=self.exchange_name, exchange_type="topic"
        )
        queue_name = self.result.method.queue
        # print('queue_name: ' + queue_name)

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
    thread_queue = Queue()
    consumer = TopicQueueConsumer(thread_queue, "connection")

    t1 = threading.Thread(target=consumer.start_consumer, args=())
    t1.start()

    while True:
        if not thread_queue.empty():
            print("-----thread-----got message: " + str(thread_queue.get()))
            print("----------")
