import pika


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
            virtual_host=self.config["virtualHost"],  # 包含交换机和队列的虚拟机名称
            credentials=credentials
        )
        return pika.BlockingConnection(parameters)

    def publish(self, message):
        try:
            connection = self._create_connection()
            channel = connection.channel()

            # 声明交换机，并不真正创建交换机
            # 创建交换机的逻辑在接受消息的类中实现
            # 如果没有对应的Consumer，在Publisher中创建交换机是没有意义的
            channel.exchange_declare(
                exchange=self.config["exchangeName"],
                passive=True
            )
            channel.basic_publish(
                exchange=self.config["exchangeName"],
                routing_key=self.config["routingKey"],
                body=message
            )
            print(" [x] Sent message %r" % message)
        except Exception as e:
            print(e)
        finally:
            if connection:
                connection.close()


config = {
    "username": "scofield",
    "password": "kingchen1990",
    "host": "localhost",
    "port": 5672,
    "virtualHost": "test",
    "exchangeName": "testExchange",
    "routingKey": "testQueue"
}


        
