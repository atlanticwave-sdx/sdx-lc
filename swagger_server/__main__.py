#!/usr/bin/env python3

import connexion

from swagger_server import encoder
from swagger_server.messaging.topic_queue_consumer import *
from swagger_server.utils.db_utils import *

from optparse import OptionParser
import argparse
import time
import threading
import logging
import json


def is_json(myjson):
    try:
        json.loads(myjson)
    except ValueError as e:
        return False
    return True


def start_consumer(thread_queue, db_instance):
    logger = logging.getLogger(__name__)
    logging.getLogger("pika").setLevel(logging.WARNING)

    MESSAGE_ID = 0
    HEARTBEAT_ID = 0

    rpc = TopicQueueConsumer(thread_queue, "connection")
    t1 = threading.Thread(target=rpc.start_consumer, args=())
    t1.start()

    while True:
        if not thread_queue.empty():
            msg = thread_queue.get()

            # if 'Heart Beat' in str(msg):
            #     HEARTBEAT_ID += 1
            #     logger.debug('Heart beat received. ID: ' + str(HEARTBEAT_ID))
            # else:
            #     logger.info("MQ received message:" + str(msg))
            #     logger.info('Saving to database.')
            #     if is_json(msg):
            #         if 'version' in str(msg):
            #             msg_json = json.loads(msg)
            #             msg_id = msg_json["id"]
            #             lc_name = msg_json["name"]
            #             msg_version = msg_json["version"]
            #             db_msg_id = str(lc_name) + "-" + str(msg_id) + "-" + str(msg_version)
            #             # print("msg_id: " + db_msg_id)
            #             db_instance.add_key_value_pair_to_db(db_msg_id, msg)
            #             logger.info('Save to database complete.')
            #             logger.info('message ID:' + str(db_msg_id))
            #             value = db_instance.read_from_db(db_msg_id)
            #             logger.info('got value back:')
            #             logger.info(value)
            #         else:
            #             logger.info('got message: ' + str(msg))
            #     else:
            #         db_instance.add_key_value_pair_to_db(MESSAGE_ID, msg)

            #         logger.info('Save to database complete.')
            #         logger.info('message ID:' + str(MESSAGE_ID))
            #         value = db_instance.read_from_db(MESSAGE_ID)
            #         logger.info('got value back:')
            #         logger.info(value)
            #         MESSAGE_ID += 1


def main():
    # Sleep 7 seconds waiting for RabbitMQ to be ready
    # time.sleep(7)

    logging.basicConfig(level=logging.INFO)

    # Run swagger service
    app = connexion.App(__name__, specification_dir="./swagger/")
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api("swagger.yaml", arguments={"title": "SDX LC"}, pythonic_params=True)
    # app.run(port=8080)
    # Run swagger in a thread
    threading.Thread(target=lambda: app.run(port=8080)).start()
    # app.run(port=8080)

    DB_NAME = os.environ.get("DB_NAME") + ".sqlite3"
    MANIFEST = os.environ.get("MANIFEST")

    # manifest_data = json.load(MANIFEST)
    # print(manifest_data)

    # Get DB connection and tables set up.
    db_tuples = [("config_table", "test-config")]

    db_instance = DbUtils()
    db_instance._initialize_db(DB_NAME, db_tuples)
    # amqp_url = 'amqp://guest:guest@aw-sdx-monitor.renci.org:5672/%2F'
    thread_queue = Queue()
    start_consumer(thread_queue, db_instance)


if __name__ == "__main__":
    main()
