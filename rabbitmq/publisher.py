import time
import json
import pika
from config import config


class Publisher:

    def __init__(self, config):
        self.config = config  # 字典

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

    def publish(self, message):
        try:
            connection = self._create_connection()
            channel = connection.channel()

            # 声明交换机，若交换机不存在引发异常
            # 创建交换机的逻辑在消费者程序中实现
            # 如果没有对应的消费者，生产者创建交换机是没有意义的
            channel.exchange_declare(
                exchange=self.config["exchangeName"],
                passive=True  # 仅检测交换机是否存在
            )
            channel.basic_publish(
                exchange=self.config["exchangeName"],
                routing_key=self.config["routingKey"],
                body=message
            )
            print("Sent message %r" % message)
        except Exception as e:
            print(e)
        finally:
            if connection:
                connection.close()


if __name__ == "__main__":

    p = Publisher(config)

    while True:
        time.sleep(3)
        msg = json.dumps({"name": "scofield", "age": 18})
        p.publish(msg)