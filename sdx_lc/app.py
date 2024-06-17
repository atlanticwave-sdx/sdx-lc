#!/usr/bin/env python3

import argparse
import json
import logging
import os
import threading
import time
from optparse import OptionParser
from subprocess import call

import connexion

from sdx_lc import encoder
from sdx_lc.messaging.topic_queue_consumer import *
from sdx_lc.utils.db_utils import *

logger = logging.getLogger(__name__)
logging.getLogger("pika").setLevel(logging.WARNING)
LOG_FILE = os.environ.get("LOG_FILE")


def is_json(myjson):
    try:
        json.loads(myjson)
    except ValueError as e:
        return False
    return True


def start_consumer(thread_queue, db_instance):
    """
    Accept connection (also called link) messages from SDX Controller.

    :param thread_queue: TODO: unsure what this is used for.
    :param db_instance: TODO: this appears to be unused in this
        function.
    """

    MESSAGE_ID = 0
    HEARTBEAT_ID = 0

    rpc = TopicQueueConsumer(thread_queue=thread_queue, exchange_name="connection")
    t1 = threading.Thread(target=rpc.start_consumer, args=())
    t1.start()


def start_pull_topology_change():
    # Run pull_topo_job as a sub process, so if sdx-lc was killed,
    # pull_topo_job will continue to run as a independent process
    call(["python", "sdx_lc/jobs/pull_topo_changes.py"])


def main():
    if LOG_FILE:
        logging.basicConfig(filename=LOG_FILE, level=logging.INFO)
    else:
        logging.basicConfig(level=logging.INFO)

    # Run swagger service
    app = connexion.App(__name__, specification_dir="./swagger/")
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api("swagger.yaml", arguments={"title": "SDX LC"}, pythonic_params=True)

    # Run swagger in a thread
    threading.Thread(
        target=lambda: app.run(port=os.getenv("SDXLC_PORT") or 8080)
    ).start()

    # Start pulling topology changes from domain controller in a
    # separate subprocess
    processThread = threading.Thread(target=start_pull_topology_change)
    processThread.start()

    # Get DB connection and tables set up.
    db_instance = DbUtils()
    db_instance.initialize_db()
    thread_queue = Queue()
    start_consumer(thread_queue, db_instance)


if __name__ == "__main__":
    main()
