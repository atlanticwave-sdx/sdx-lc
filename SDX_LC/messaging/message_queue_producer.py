import json

import pika


class RabbitMqParams:
    def __init__(
        self,
        queue="hello",
        host="localhost",
        routingKey="hello",
        exchange="",
    ):
        # Configure Rabbit Mq Server
        self.queue = queue
        self.host = host
        self.routingKey = routingKey
        self.exchange = exchange


class RabbitMq:
    def __init__(self, params):
        self.params = params
        self._connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.params.host)
        )
        self._channel = self._connection.channel()

    def publish(self, body={}):
        result = self._channel.queue_declare(queue=self.server.queue)
        callback_queue = result.method.queue
        self._channel.basic_publish(
            exchange=self.params.exchange,
            routing_key=self.params.routingKey,
            properties=pika.BasicProperties(
                reply_to=callback_queue,
            ),
            body=str(body),
        )

        print("Published Message: {}".format(body))

        self._connection.close()


if __name__ == "__main__":
    params = RabbitMqParams(
        queue="hello", host="localhost", routingKey="hello", exchange=""
    )

    with open("./mq-test/local-ctlr-1/local-ctlr-1.manifest") as f:
        data = json.load(f)
        RabbitMq(params).publish(body=data)
