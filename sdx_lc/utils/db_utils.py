import logging
import os
from urllib.parse import urlparse

import pymongo

DB_NAME = os.environ.get("DB_NAME")
DB_CONFIG_TABLE_NAME = os.environ.get("DB_CONFIG_TABLE_NAME")


def obfuscate_password_in_uri(uri: str) -> str:
    """
    Replace password field in URIs with a `*`, for logging.
    """
    parts = urlparse(uri)
    if parts.password:
        return f"{parts.scheme}://{parts.username}:*@{parts.hostname}:{parts.port}/"
    else:
        return uri


class DbUtils(object):
    def __init__(self):
        self.db_name = DB_NAME
        self.config_table_name = DB_CONFIG_TABLE_NAME

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        mongo_user = os.getenv("MONGO_USER") or "guest"
        mongo_pass = os.getenv("MONGO_PASS") or "guest"
        mongo_host = os.getenv("MONGO_HOST")
        mongo_port = os.getenv("MONGO_PORT")

        if mongo_host is None:
            mongo_connstring = os.getenv("MONGODB_CONNSTRING")
            if mongo_connstring is None:
                raise Exception("Neither MONGO_HOST nor MONGODB_CONNSTRING is set")

        if mongo_port is None:
            raise Exception("MONGO_PORT environment variable is not set")
        else:
            mongo_connstring = (
                f"mongodb://{mongo_user}:{mongo_pass}@{mongo_host}:{mongo_port}/"
            )

        # Log DB URI, without a password.
        self.logger.info(f"[DB] Using {obfuscate_password_in_uri(mongo_connstring)}")

        self.mongo_client = pymongo.MongoClient(mongo_connstring)

    def initialize_db(self):
        """Init database"""
        self.logger.debug("Trying to load {} from DB".format(self.db_name))

        if self.db_name not in self.mongo_client.list_database_names():
            self.logger.debug(
                "No existing {} from DB, creating table".format(self.db_name)
            )
            self.sdxdb = self.mongo_client[self.db_name]
            self.logger.debug("DB {} initialized".format(self.db_name))

        self.sdxdb = self.mongo_client[self.db_name]
        config_col = self.sdxdb[self.config_table_name]
        self.logger.debug("DB {} initialized".format(self.db_name))

    def add_key_value_pair_to_db(self, key, value):
        """Add key value pair to database"""
        key = str(key)
        obj = self.read_from_db(key)
        if obj is None:
            self.logger.debug("Adding key value pair to DB.")
            return self.sdxdb[self.db_name][self.config_table_name].insert_one(
                {key: value}
            )

        query = {"_id": obj["_id"]}
        self.logger.debug("Updating DB entry.")
        result = self.sdxdb[self.db_name][self.config_table_name].replace_one(
            query, {key: value}
        )
        return result

    def read_from_db(self, key):
        """Given a user specified key, return the value stored in database"""
        key = str(key)
        return self.sdxdb[self.db_name][self.config_table_name].find_one(
            {key: {"$exists": 1}}
        )
