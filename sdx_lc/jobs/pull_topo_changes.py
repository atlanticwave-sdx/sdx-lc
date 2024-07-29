import argparse
import json
import logging
import os.path
import sys
import threading
import time
import urllib.request

# append abspath, so this file can import other modules from parent directory
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
)

from messaging.rpc_queue_producer import RpcProducer
from utils.db_utils import DbUtils

OXP_PULL_URL = os.environ.get("OXP_PULL_URL")
OXP_PULL_INTERVAL = os.environ.get("OXP_PULL_INTERVAL")
logger = logging.getLogger(__name__)


def main():
    db_instance = DbUtils()
    db_instance.initialize_db()

    process_domain_controller_topo(db_instance)


def process_domain_controller_topo(db_instance):
    while True:
        latest_topology_exists = False
        latest_topology = db_instance.read_from_db("latest_topology")

        if latest_topology:
            latest_topology_exists = True
            try:
                json_latest_topology = json.loads(latest_topology["latest_topology"])
            except ValueError:
                logger.debug("Got invalid JSON topology. Ignored.")
                continue

            try:
                latest_topo_version = json_latest_topology["version"]
            except KeyError:
                logger.debug("Error getting topo version")
                continue
        else:
            logger.debug("Latest topology does not exist")

        try:
            pulled_topology = urllib.request.urlopen(OXP_PULL_URL).read()
        except (urllib.request.URLError, ConnectionResetError):
            logger.debug("Error connecting to domain controller...")
            time.sleep(int(OXP_PULL_INTERVAL))
            continue

        if not pulled_topology:
            time.sleep(int(OXP_PULL_INTERVAL))
            continue

        logger.debug("Pulled request from domain controller")

        try:
            json_pulled_topology = json.loads(pulled_topology)
        except ValueError:
            logger.debug("Cannot parse pulled topology, invalid JSON")
            continue

        try:
            pulled_topo_version = json_pulled_topology["version"]
        except KeyError:
            logger.debug("Error getting topo version")
            continue

        if latest_topology_exists and latest_topo_version == pulled_topo_version:
            time.sleep(int(OXP_PULL_INTERVAL))
            continue

        logger.debug("Pulled topo with different version. Adding pulled topo to db")
        db_instance.add_key_value_pair_to_db(
            f"topoVersion{json_pulled_topology['version']}", pulled_topology
        )
        db_instance.add_key_value_pair_to_db("latest_topology", pulled_topology)
        logger.debug("Added pulled topo to db")
        # initiate rpc producer with 5 seconds timeout
        rpc_producer = RpcProducer(5, "", "topo")
        # publish topology to message queue for sdx-controller
        response = rpc_producer.call(pulled_topology)
        # Signal to end keep alive pings.
        rpc_producer.stop()

        time.sleep(int(OXP_PULL_INTERVAL))


if __name__ == "__main__":
    main()
