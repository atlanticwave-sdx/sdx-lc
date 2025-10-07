import importlib
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

CLIENT_PACKAGE = os.getenv("CLIENT_PACKAGE", None)
CLIENT_TOPOLOGY_FUNCTION = os.getenv("CLIENT_TOPOLOGY_FUNCTION", None)

OXPO_USER = os.environ.get("OXPO_USER", None)
OXPO_PASS = os.environ.get("OXPO_PASS", None)
OXP_PULL_URL = os.environ.get("OXP_PULL_URL")
OXP_PULL_INTERVAL = os.environ.get("OXP_PULL_INTERVAL")
PUB_QUEUE = MessageQueueNames.OXP_UPDATE
logger = logging.getLogger(__name__)


def main():
    db_instance = DbUtils()
    db_instance.initialize_db()

    process_domain_controller_topo(db_instance)


def process_domain_controller_topo(db_instance):
    while True:
        time.sleep(int(OXP_PULL_INTERVAL))
        latest_topology_exists = False
        latest_topology = db_instance.read_from_db(Constants.LATEST_TOPOLOGY)

        if latest_topology:
            latest_topology_exists = True
            try:
                json_latest_topology = json.loads(
                    latest_topology[Constants.LATEST_TOPOLOGY]
                )
            except ValueError:
                logger.debug("Got invalid JSON topology. Ignored.")
                continue

            try:
                if not CLIENT_PACKAGE:
                    latest_topo_version = json_latest_topology["version"]
                else:
                    client_module = importlib.import_module(CLIENT_PACKAGE)
                    topology_function = getattr(client_module, CLIENT_TOPOLOGY_FUNCTION)
                    topology_function()
            except KeyError:
                logger.debug("Error getting topo version")
                continue
        else:
            logger.debug("Latest topology does not exist")

        try:
            if not CLIENT_PACKAGE:
                response = requests.get(OXP_PULL_URL, auth=(OXPO_USER, OXPO_PASS))
                pulled_topology = response.content
            else:
                client_module = importlib.import_module(CLIENT_PACKAGE)
                topology_function = getattr(client_module, CLIENT_TOPOLOGY_FUNCTION)
                topology_function()
        except (requests.ConnectionError, requests.HTTPError):
            logger.debug("Error connecting to domain controller...")
            continue

        if not response.ok:
            continue

        logger.debug("Pulled request from domain controller")

        try:
            json_pulled_topology = response.json()
        except ValueError:
            logger.debug("Cannot parse pulled topology, invalid JSON")
            continue

        try:
            pulled_topo_version = json_pulled_topology["version"]
        except KeyError:
            logger.debug("Error getting topo version")
            continue

        if latest_topology_exists and latest_topo_version == pulled_topo_version:
            continue

        logger.debug("Pulled topo with different version. Adding pulled topo to db")
        db_instance.add_key_value_pair_to_db(
            f"{Constants.TOPOLOGY_VERSION}_{json_pulled_topology['version']}",
            json.dumps(json_pulled_topology),
        )
        db_instance.add_key_value_pair_to_db(Constants.LATEST_TOPOLOGY, pulled_topology)
        topology_ts = int(time.time())
        db_instance.add_key_value_pair_to_db(
            Constants.LATEST_TOPOLOGY_TS, str(topology_ts)
        )
        logger.debug("Added pulled topo to db")
        # initiate rpc producer with 5 seconds timeout
        rpc_producer = RpcProducer(5, "", PUB_QUEUE)
        # publish topology to message queue for sdx-controller
        _response = rpc_producer.call(json.dumps(json_pulled_topology))
        # Signal to end keep alive pings.
        rpc_producer.stop()


if __name__ == "__main__":
    main()
