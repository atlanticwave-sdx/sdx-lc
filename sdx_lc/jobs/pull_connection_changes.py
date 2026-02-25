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

SDXLC_DOMAIN = os.environ.get("SDXLC_DOMAIN")
OXP_LIST_CONNECTIONS_URL = os.environ.get("OXP_LIST_CONNECTIONS_URL")
OXP_PULL_CONNECTIONS_INTERVAL = os.environ.get("OXP_PULL_CONNECTIONS_INTERVAL")
PUB_QUEUE = MessageQueueNames.OXP_UPDATE
logger = logging.getLogger(__name__)


def main():
    db_instance = DbUtils()
    db_instance.initialize_db()
    process_oxp_connections(db_instance)


# Periodically pull l2vpn (connection) status from OXP, and handle status change.
# Possible l2vpn status are:
# “up” if the L2VPN is operational,
# “down” if the L2VPN is not operational due to topology issues/lack of path, or endpoints being down,
# “error” when there is an error with the L2VPN,
# “under provisioning” when the L2VPN is still being provisioned by the OXPs,
# “maintenance” when the L2VPN is being affected by a network maintenance.
def process_oxp_connections(db_instance):
    while True:
        time.sleep(int(OXP_PULL_CONNECTIONS_INTERVAL))
        try:
            try:
                response = requests.get(OXP_LIST_CONNECTIONS_URL, timeout=10)
                connections = response.content
                assert response.ok, response.text
            except (requests.ConnectionError, requests.HTTPError) as err:
                logger.error(f"Error connecting to OXP: {err}")
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
                logger.info(
                    f"Status change for {service_id}: "
                    f"{existing_connection_status} changed to {new_status}"
                )
                db_instance.add_key_value_pair_to_db(service_id, existing_connection_json)
                rpc_msg = {
                    "lc_domain": SDXLC_DOMAIN,
                    "msg_type": "oxp_conn_status_change",
                    "service_id": service_id,
                    "existing_status": existing_connection_status,
                    "new_status": new_status,
                }
                rpc_producer = RpcProducer(5, "", PUB_QUEUE)
                rpc_producer.call(json.dumps(rpc_msg))
                rpc_producer.stop()
        except Exception:
            logger.exception(
                "Unexpected error while processing OXP connections; Retrying."
            )


if __name__ == "__main__":
    main()
