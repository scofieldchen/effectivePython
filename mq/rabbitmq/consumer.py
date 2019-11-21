import json
import pika
import config


class Consumer:

    def __init__(self, config):
        self.config = config  # 字典

    def __enter__(self):
        self.connection = self._create_connection()
        return self

    def __exit__(self, *args):
        self.connection.close()

    def _create_connection(self):
        credentials = pika.PlainCredentials(
            username=self.config["username"],
            password=self.config["password"]
        )
        parameters = pika.ConnectionParameters(
            host=self.config["host"],
            port=self.config["port"],
            virtual_host=self.config["virtualHost"],
            credentials=credentials
        )
        return pika.BlockingConnection(parameters)

    def _create_exchange(self, channel):
        exchange_options = self.config["exchangeOptions"]
        channel.exchange_declare(
            exchange=self.config["exchangeName"],
            exchange_type=self.config["exchangeType"],
            passive=exchange_options["passive"],
            durable=exchange_options["durable"],
            auto_delete=exchange_options["autoDelete"],
            internal=exchange_options["internal"]
        )

    def _create_queue(self, channel):
        queue_options = self.config["queueOptions"]
        channel.queue_declare(
            queue=self.config['queueName'],
            passive=queue_options['passive'], 
            durable=queue_options['durable'],
            exclusive=queue_options['exclusive'],
            auto_delete=queue_options['autoDelete']
        )

    def _consume_message(self, channel, method, properties, body):
        self.callback(body)
        channel.basic_ack(delivery_tag=method.delivery_tag)

    def consume(self, callback):
        """callback: 回调函数，处理消息的逻辑"""
        self.callback = callback
        channel = self.connection.channel()

        self._create_exchange(channel)
        self._create_queue(channel)

        channel.queue_bind(
            queue=self.config['queueName'],
            exchange=self.config['exchangeName'],
            routing_key=self.config['routingKey']
        )

        channel.basic_consume(
            queue=self.config["queueName"],
            on_message_callback=self._consume_message
        )
        channel.start_consuming()


if __name__ == "__main__":

    # 回调函数
    def process_msg(msg):
        data = json.loads(msg)
        print(data)

    with Consumer(config.RABBIT) as consumer:
        consumer.consume(process_msg)