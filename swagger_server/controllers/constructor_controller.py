""" constructor controller """
import connexion
import pika

from swagger_server.models.constructor import Constructor  # noqa: E501
from swagger_server.models.error_message import ErrorMessage  # noqa: E501
from swagger_server.util import util


def build_topology(body):  # noqa: E501
    """Send a new topology or update to SDX-LC

    Build a topology # noqa: E501

    :param body: placed for adding or update a new topology
    :type body: dict | bytes

    :rtype: Constructor
    """
    body = {}
    if connexion.request.is_json:
        body = Constructor.from_dict(connexion.request.get_json())  # noqa: E501
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
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
    return " [x] Sent: %s" % cmd
    return body
