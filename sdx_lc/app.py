#!/usr/bin/env python3

import logging
import os
import threading
from queue import Queue
from subprocess import call

import connexion
from asgiref.wsgi import WsgiToAsgi
from flask import redirect

from sdx_lc import encoder
from sdx_lc.messaging.topic_queue_consumer import TopicQueueConsumer
from sdx_lc.utils.db_utils import DbUtils


def start_consumer(thread_queue, db_instance):
    """
    Accept connection (also called link) messages from SDX Controller.

    :param thread_queue: TODO: unsure what this is used for.
    :param db_instance: TODO: this appears to be unused in this
        function.
    """

    rpc = TopicQueueConsumer(thread_queue=thread_queue, exchange_name="connection")
    t1 = threading.Thread(target=rpc.start_consumer, args=())
    t1.start()


def start_pull_topology_change():
    # Run pull_topo_job as a sub process, so if sdx-lc was killed,
    # pull_topo_job will continue to run as a independent process
    call(["python", "sdx_lc/jobs/pull_topo_changes.py"])


def create_app():
    """
    Create a Flas/Connexion App.
    """

    logger = logging.getLogger(__name__)
    logging.getLogger("pika").setLevel(logging.WARNING)

    log_file = os.environ.get("LOG_FILE")

    if log_file:
        logging.basicConfig(filename=log_file, level=logging.INFO)
    else:
        logging.basicConfig(level=logging.INFO)

    # Run swagger service
    app = connexion.App(__name__, specification_dir="./swagger/")
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api("swagger.yaml", arguments={"title": "SDX LC"}, pythonic_params=True)

    # Start pulling topology changes from domain controller in a
    # separate subprocess
    processThread = threading.Thread(target=start_pull_topology_change)
    processThread.start()

    # Get DB connection and tables set up.
    db_instance = DbUtils()
    db_instance.initialize_db()

    # Consume connection/link messages
    thread_queue = Queue()
    start_consumer(thread_queue, db_instance)

    return app.app


# We can run the app using flask, like so:
#
#     $ flask --app sdx_lc.app:app run --debug
#
# Or with an WSGI server such as gunicorn:
#
#     $ gunicorn --bind localhost:$SDXLC_PORT sdx_lc.app:app
#
app = create_app()

# We use WsgiToAsgi adapter so that we can use an ASGI server (such as
# uvicorn or hypercorn), like so:
#
#     $ uvicorn sdx_lc.app:asgi_app --host 0.0.0.0 --port 8080
#
asgi_app = WsgiToAsgi(app)


# Set up a redirect for convenience.
@app.route("/", methods=["GET"])
def index():
    return redirect("/SDX-LC/2.0.0/ui/")


if __name__ == "__main__":
    app.run(port=os.getenv("SDXLC_PORT") or 8080)
