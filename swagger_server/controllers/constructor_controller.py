""" constructor controller """
from datetime import datetime
import logging
import os
import connexion
import pika
import pytz
import requests

from swagger_server import settings  # pylint: disable=E0401
from swagger_server.models.constructor import Constructor  # noqa: E501
from swagger_server.models.parse_topology import (ParseTopology)  # noqa: E501
# from swagger_server.models.error_message import ErrorMessage  # noqa: E501
from swagger_server.utils import topology_mock \
        # pylint: disable=E0401

OXPO = os.environ.get("SDX_OXPO")
OXP_NAME= os.environ.get("SDX_NAME")
MODEL_VERSION= os.environ.get("SDX_VERSION")
OXP_URL= os.environ.get("SDX_URL")


def get_timestamp(timestamp=None):
    """Function to obtain the current time_stamp in a specific format"""
    if timestamp is not None:
        if isinstance(timestamp, datetime):
            timestamp = timestamp.strftime("%Y-%m-%dT%H:%M:%SZ")
        elif len(timestamp) >= 19:
            timestamp = timestamp[:10]+"T"+timestamp[11:19]+"Z"
    else:
        timestamp = datetime.now(
            pytz.timezone("America/New_York")).strftime("%Y-%m-%dT%H:%M:%SZ")
    return timestamp


def message_queue(cmd):
    """ Rabbit MQ producer function """
    credentials = pika.PlainCredentials('mq_user', 'mq_pwd')
    connection = pika.BlockingConnection(
            pika.ConnectionParameters('rabbitmq3', 5672, '/', credentials))
    channel = connection.channel()
    channel.queue_declare(queue='task_queue', durable=True)
    channel.basic_publish(
        exchange='',
        routing_key='task_queue',
        body=cmd,
        properties=pika.BasicProperties(
            delivery_mode=2,  # make message persistent
        ))
    connection.close()
    return f" [x] Sent: {cmd}"


def kytos_event_info(body):  # pylint: disable=W0613
    """ Function meant describe event """
    logging.debug("######### event_topology #########")
    admin_events = [
            "kytos/topology.switch.enabled",
            "kytos/topology.switch.disabled"]
    operational_events = [
            "kytos/topology.link_up",
            "kytos/topology.link_down"]
    event = body["event"]
    topology = body["topology"]
    if event.name in admin_events:
        event_type = 1
    elif event.name in operational_events and event.timestamp is not None:
        event_type = 2
    else:
        event_type = 0
        topology = topology_mock.topology_mock()
    topology_info = {
            "event": event,
            "event_type": event_type,
            "event_name": event.name,
            "timestamp": event.timestamp,
            "topology": topology}
    logging.debug(topology_info)
    return topology_info


def build_topology(body=None):  # noqa: E501
    """Send a new topology or update to SDX-LC

    Build a topology # noqa: E501

    :param body: placed for adding or update a new topology
    :type body: dict | bytes

    :rtype: Constructor
    """
    logging.debug("######### build_topology #########")
    if connexion.request.is_json:
        body = Constructor.from_dict(connexion.request.get_json())  # noqa: E501
        logging.debug(body)
        try:
            if OXPO == "kytos":
                topology_info = kytos_event_info(body)
                if not topology_info["timestamp"]:
                    timestamp = get_timestamp()
                else:
                    timestamp = get_timestamp(topology_info["timestamp"])
                topology_update = ParseTopology(
                        topology=topology_info["topology"],
                        version=1,
                        timestamp=timestamp,
                        model_version=MODEL_VERSION,
                        oxp_name=OXP_NAME,
                        oxp_url=OXP_URL,
                        ).get_sdx_topology()
                topology_dict = {
                        "id": topology_update["id"],
                        "name": topology_update["name"],
                        "version": topology_update["version"],
                        "model_version": topology_update["model_version"],
                        "timestamp": topology_update["timestamp"],
                        "nodes": topology_update["nodes"],
                        "links": topology_update["links"],
                        }
            else:
                topology_dict = topology_mock.topology_mock()
            logging.debug("######### topology_update #########")
            logging.debug(topology_update)
            validate_topology = requests.post(
                    settings.VALIDATE_TOPOLOGY, json=topology_dict)
            if validate_topology.status_code == 200:
                requests.post(settings.SDX_TOPOLOGY, json=topology_dict)
                return (topology_dict, 200)
            return (validate_topology.json(), 400)
        except Exception as err:  # pylint: disable=W0703
            return (err, "Validation Error", 400)
    logging.debug("######### json format error #########")
    return ("json format error", 400)
