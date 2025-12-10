import json
import logging
import os.path
import sys
import time

import requests
from sdx_datamodel.constants import Constants, MessageQueueNames

# append abspath, so this file can import other modules from parent directory
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
)

from messaging.rpc_queue_producer import RpcProducer
from utils.db_utils import DbUtils

OXPO_USER = os.environ.get("OXPO_USER", None)
OXPO_PASS = os.environ.get("OXPO_PASS", None)
OXP_LIST_CONNECTIONS_URL = os.environ.get("OXP_LIST_CONNECTIONS_URL")
OXP_PULL_CONNECTIONS_INTERVAL = os.environ.get("OXP_PULL_CONNECTIONS_INTERVAL")
PUB_QUEUE = MessageQueueNames.OXP_UPDATE
logger = logging.getLogger(__name__)


def main():
    db_instance = DbUtils()
    db_instance.initialize_db()
    process_oxp_connections(db_instance)


def process_oxp_connections(db_instance):
    while True:
        time.sleep(int(OXP_PULL_CONNECTIONS_INTERVAL))

        try:
            response = requests.get(OXP_LIST_CONNECTIONS_URL)
            connections = response.content
        except (requests.ConnectionError, requests.HTTPError):
            logger.debug("Error connecting to OXP...")
            continue

        if not response.ok:
            continue

        logger.debug("Received connections from OXP.")

        try:
            connections_json = response.json()
        except ValueError:
            logger.debug("Cannot parse connections, invalid JSON.")
            continue

        if not connections_json:
            logger.debug("No connections yet.")
            continue

        for service_id, connection in connections_json.items():
            # Fetch existing connection from DB
            existing_connection = db_instance.get_value_by_key(service_id)

            if not existing_connection:
                logger.debug(f"New connection {service_id}, ignored")
                continue

            try:
                existing_connection_json = json.loads(existing_connection)
            except ValueError:
                logger.debug(f"Invalid JSON in DB for {service_id}")
                continue

            existing_connection_status = (
                existing_connection_json.get("status")
                if existing_connection_json
                else None
            )
            new_status = connection.get("status")

            if existing_connection_status == new_status:
                logger.debug(f"Status unchanged for {service_id}")
                continue

            existing_connection_json["status"] = new_status
            logger.debug(
                f"Status change for {service_id}: "
                f"{existing_connection_status} changed to {new_status}"
            )
            db_instance.add_key_value_pair_to_db(service_id, existing_connection_json)

            rpc_producer = RpcProducer(5, "", PUB_QUEUE)
            rpc_producer.call(json.dumps(existing_connection_json))
            rpc_producer.stop()


if __name__ == "__main__":
    main()
