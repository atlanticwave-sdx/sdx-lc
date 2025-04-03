import json
import logging
import os

import requests
from sdx_datamodel.constants import MessageQueueNames

from sdx_lc.messaging.rpc_queue_producer import RpcProducer
from sdx_lc.utils.db_utils import DbUtils

logger = logging.getLogger(__name__)

OXP_USER = os.environ.get("OXP_USER", None)
OXP_PASS = os.environ.get("OXP_PASS", None)
OXP_CONNECTION_URL = os.environ.get("OXP_CONNECTION_URL")
SDXLC_DOMAIN = os.environ.get("SDXLC_DOMAIN", "")
PUB_QUEUE = MessageQueueNames.OXP_UPDATE


def is_json(myjson):
    try:
        json.loads(myjson)
    except ValueError as e:
        return False
    return True


class SdxControllerMsgHandler:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        # Get DB connection and tables set up.
        self.db_instance = DbUtils()
        self.db_instance.initialize_db()
        self.heartbeat_id = 0
        self.message_id = 0

    def send_conn_response_to_sdx_controller(self, service_id, operation, oxp_response):
        oxp_response_json = oxp_response.json()
        rpc_msg = {
            "lc_domain": SDXLC_DOMAIN,
            "msg_type": "oxp_conn_response",
            "service_id": service_id,
            "operation": operation,
            "oxp_response_code": oxp_response.status_code,
            "oxp_response": oxp_response_json,
        }
        self.rpc_producer = RpcProducer(5, "", PUB_QUEUE)
        response = self.rpc_producer.call(json.dumps(rpc_msg))
        self.rpc_producer.stop()
        self.logger.debug(
            f"Sent OXP connection response to SDX controller via MQ. MQ response: {response}"
        )

    def process_sdx_controller_json_msg(self, msg):
        if "Heart Beat" in str(msg):
            self.heartbeat_id += 1
            self.logger.debug("Heart beat received. ID: " + str(self.heartbeat_id))
            return

        self.logger.info("MQ received message:" + str(msg))

        if not is_json(msg):
            self.logger.info("Other type of message")
            self.db_instance.add_key_value_pair_to_db(self.message_id, msg)
            self.logger.info("Save to database complete.")
            self.logger.info("Message ID:" + str(self.message_id))
            self.message_id += 1
            return

        msg_json = json.loads(msg)

        if (
            "link" in msg_json
            and "uni_a" in msg_json["link"]
            and "uni_z" in msg_json["link"]
        ):
            service_id = msg_json.get("service_id")
            connection = msg_json.get("link")
            self.logger.info("Got connection message.")
            self.db_instance.add_key_value_pair_to_db(self.message_id, connection)
            self.logger.info("Save to database complete.")
            self.logger.info("Message ID:" + str(self.message_id))
            self.message_id += 1
            self.logger.info("Sending connection info to OXP.")
            # send connection info to OXP
            if msg_json.get("operation") == "post":
                try:
                    oxp_response = requests.post(
                        str(OXP_CONNECTION_URL),
                        json=connection,
                        auth=(OXP_USER, OXP_PASS),
                    )
                except Exception as e:
                    self.logger.error(f"Error on POST to {OXP_CONNECTION_URL}: {e}")
                    self.logger.info(
                        "Check your configuration and make sure OXP service is running."
                    )
                self.logger.info(
                    f"Status from OXP: {oxp_response} - {oxp_response.text}"
                )
                self.send_conn_response_to_sdx_controller(
                    service_id, msg_json["operation"], oxp_response
                )
            elif msg_json.get("operation") == "delete":
                try:
                    oxp_response = requests.delete(
                        str(OXP_CONNECTION_URL),
                        json=connection,
                        auth=(OXP_USER, OXP_PASS),
                    )
                except Exception as e:
                    self.logger.error(f"Error on DELETE {OXP_CONNECTION_URL}: {e}")
                    self.logger.info(
                        "Check your configuration and make sure OXP service is running."
                    )
                self.logger.info(
                    f"Status from OXP: {oxp_response} - {oxp_response.text}"
                )
                self.send_conn_response_to_sdx_controller(
                    service_id, msg_json["operation"], oxp_response
                )
        elif "version" in msg_json:
            msg_id = msg_json["id"]
            lc_name = msg_json["name"]
            msg_version = msg_json["version"]
            db_msg_id = str(lc_name) + "-" + str(msg_id) + "-" + str(msg_version)
            self.db_instance.add_key_value_pair_to_db(db_msg_id, msg)
            self.logger.info("Save to database complete.")
            self.logger.info("message ID:" + str(db_msg_id))
        else:
            self.logger.info("Got message: " + str(msg))
