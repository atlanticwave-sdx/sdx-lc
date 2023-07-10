#!/usr/bin/env python3

import logging

import connexion

from swagger_server import encoder
from swagger_server.utils.db_utils import DbUtils

logging.basicConfig(level=logging.INFO)

# Run swagger service
app = connexion.App(__name__, specification_dir="./swagger/")
app.app.json_encoder = encoder.JSONEncoder
app.add_api("swagger.yaml", arguments={"title": "SDX LC"}, pythonic_params=True)
# gunicorn_logger = logging.getLogger('gunicorn.error')
# app.logger.handlers = gunicorn_logger.handlers
# app.logger.setLevel(gunicorn_logger.level)


# Get DB connection and tables set up.
db_instance = DbUtils()
db_instance.initialize_db()


if __name__ == "__main__":
    app.run(host="0.0.0.0")
