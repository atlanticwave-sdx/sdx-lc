import pika


class MetaClass(type):
    _instance = {}

    def __call__(cls, *args, **kwargs):
        """Singelton Design Pattern"""

        if cls not in cls._instance:
            cls._instance[cls] = super(MetaClass, cls).__call__(*args, **kwargs)
            return cls._instance[cls]


class RabbitmqConfigure(metaclass=MetaClass):
    def __init__(
        self, queue="hello", host="localhost", routingKey="hello", exchange=""
    ):
        """Configure Rabbit Mq Server"""
        self.queue = queue
        self.host = host
        self.routingKey = routingKey
        self.exchange = exchange


class RabbitMq:
    def __init__(self, server):
        """

        :param server: Object of class RabbitmqConfigure
        """

        self.server = server

        self._connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.server.host)
        )
        self._channel = self._connection.channel()
        self._channel.queue_declare(queue=self.server.queue)

    def publish(self, msg={}):
        """

        :param msg: JSON msg
        :return: None
        """

        self._channel.basic_publish(
            exchange=self.server.exchange,
            routing_key=self.server.routingKey,
            body=str(msg),
        )

        print("Published Message: {}".format(msg))
        self._connection.close()


if __name__ == "__main__":
    server = RabbitmqConfigure(
        queue="hello", host="localhost", routingKey="hello", exchange=""
    )

    rabbitmq = RabbitMq(server)
    rabbitmq.publish(msg={"localctlr": 1})
