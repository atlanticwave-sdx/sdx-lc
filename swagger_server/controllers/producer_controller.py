""" MQ producer controller """
import connexion
import pika

from swagger_server.models.job import Job  # noqa: E501


def push_message(cmd):  # noqa: E501
    """Send a new message to Rabbit MQ

    Produce a Queue Message # noqa: E501

    :param body: placed for adding or updating a new message
    :type body: dict | bytes

    :rtype: Job
    """
    if connexion.request.is_json:
        cmd = Job.from_dict(connexion.request.get_json())  # noqa: E501
        credentials = pika.PlainCredentials("mq_user", "mq_pwd")
        connection = pika.BlockingConnection(
            pika.ConnectionParameters("rabbitmq3", 5672, "/", credentials)
        )
        channel = connection.channel()
        channel.queue_declare(queue="task_queue", durable=True)
        channel.basic_publish(
            exchange="",
            routing_key="task_queue",
            body=cmd,
            properties=pika.BasicProperties(
                delivery_mode=2,  # make message persistent
            ),
        )
        connection.close()
    return f" [x] Sent: {cmd}"
