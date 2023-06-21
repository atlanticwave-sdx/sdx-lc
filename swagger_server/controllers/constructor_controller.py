""" constructor controller """
import connexion
import pika

from swagger_server.models.constructor import Constructor  # noqa: E501
from swagger_server.models.parse_topology import (ParseTopology)  # noqa: E501
# from swagger_server.models.error_message import ErrorMessage  # noqa: E501
from swagger_server.utils import sdx_utils, topology_mock \
        # pylint: disable=E0401

SDX_TOPOLOGY_API = "http://0.0.0.0:8181/api/kytos/sdx_topology/v1"
VALIDATE_TOPOLOGY = "http://0.0.0.0:8181/api/kytos/sdx_topology/v1/validate"


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


def create_update_topology(self, event_type=0, event_timestamp=None):
    """ Create topology """
    try:
        if event_type != 0:
            event_timestamp = sdx_utils.get_timestamp(event_timestamp)
            topology_update = ParseTopology(
                    topology=self.get_kytos_topology(),
                    version=1,
                    timestamp=event_timestamp,
                    model_version="2.0.0",
                    oxp_name="AmLight-OXP",
                    oxp_url="amlight.net",
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
        # validate_topology = requests.post(VALIDATE_TOPOLOGY, json=topology_dict)
        # if validate_topology.status_code == 200:
        # else
            #return (validate_topology.json(), 400)
        return (topology_dict, 200)
    except Exception as err:  # pylint: disable=W0703
        return (err, "Validation Error", 400)


def build_topology(body):  # noqa: E501
    """Send a new topology or update to SDX-LC

    Build a topology # noqa: E501

    :param body: placed for adding or update a new topology
    :type body: dict | bytes

    :rtype: Constructor
    """
    if connexion.request.is_json:
        body = Constructor.from_dict(connexion.request.get_json())  # noqa: E501
    return body
