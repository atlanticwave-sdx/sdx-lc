import json
import logging
import requests
import os

logger = logging.getLogger(__name__)

OXP_CONNECTION_URL = os.environ.get("OXP_CONNECTION_URL")


def is_json(myjson):
    try:
        json.loads(myjson)
    except ValueError as e:
        return False
    return True


class SdxControllerMsgHandler:
    def __init__(self, db_instance):
        self.db_instance = db_instance

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

        self.logger.info("JSON message")
        msg_json = json.loads(msg)
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
                    r = requests.post(str(OXP_CONNECTION_URL), json=connection)
                    self.logger.info(f"Status from OXP: {r}")
                except Exception as e:
                    self.logger.error(f"Error on POST to {OXP_CONNECTION_URL}: {e}")
                    self.logger.info(
                        "Check your configuration and make sure OXP service is running."
                    )
            elif msg_json.get("operation") == "delete":
                try:
                    r = requests.delete(str(OXP_CONNECTION_URL), json=connection)
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
            self.db_instance.add_key_value_pair_to_db(db_msg_id, msg)
            self.logger.info("Save to database complete.")
            self.logger.info("message ID:" + str(db_msg_id))
        else:
            self.logger.info("Got message: " + str(msg))
