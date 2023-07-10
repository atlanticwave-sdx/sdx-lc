""" Mongodb Connection """
import logging
import os

import pymongo

USER_NAME = os.environ.get("SDXLC_MONGO_USERNAME")
PASSWORD = os.environ.get("SDXLC_MONGO_PASSWORD")
DB_NAME = os.environ.get("SDXLC_MONGO_DB")
TOPO_COLL = os.environ.get("SDXLC_MONGO_COLLECTION")
MONGODB_CONNSTRING = os.environ.get("MONGODB_CONNSTRING")


class DbUtils(object):
    """mongodb instance"""

    def __init__(self):
        self.db_name = DB_NAME
        self.config_topo_coll = TOPO_COLL
        self.mongo_client = pymongo.MongoClient(MONGODB_CONNSTRING)
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

    def initialize_db(self):
        """Init database"""
        message = f"Trying to load {self.db_name} from DB"
        self.logger.debug(message)

        if self.db_name not in self.mongo_client.list_database_names():
            message = f"{self.db_name} do not  exist in DB, creating table"
            self.logger.debug(message)
        self.sdxdb = self.mongo_client[self.db_name]  # pylint: disable=W0201
        self.topo_coll = self.sdxdb[self.config_topo_coll]  # pylint: disable=W0201
        message = f"DB {self.db_name} initialized"
        self.logger.debug(message)

    def add_key_value_pair_to_db(self, key, value):
        """Add key value pair to database"""
        key = str(key)
        obj = self.read_from_db(key)
        if obj is None:
            self.logger.debug("Adding key value pair to DB.")
            return self.sdxdb[self.topo_coll].insert_one({key: value})

        query = {"_id": obj["_id"]}
        self.logger.debug("Updating DB entry.")
        result = self.sdxdb[self.topo_coll].replace_one(query, {key: value})
        return result

    def read_from_db(self, key):
        """Given a user specified key, return the value stored in database"""
        key = str(key)
        return self.sdxdb[self.topo_coll].find_one({key: {"$exists": 1}})
