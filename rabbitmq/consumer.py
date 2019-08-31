import pika


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
    
    # RMQ配置
    config = {
        # 身份认证
        "username": "guest",
        "password": "guest",
        
        # 连接参数
        "host": "localhost",        # 终端
        "port": 5672,               # 端口，默认5672
        "virtualHost": "/",         # 虚拟机，username=guest使用默认虚拟机'/'
        
        # 交换机设置
        "exchangeName": "testExchange",  # 交换机名称
        "exchangeType": "direct",        # 交换机类型，'fanout','direct','topic'
        "exchangeOptions": {
            "passive": False,            # True:仅检查交换机是否存在, False:若不存在则创建交换机
            "durable": True,             # True:RMQ重启后保留交换机(持久化), False:RMQ重启后删除交换机
            "autoDelete": False,         # True:当所有队列与交换机解绑后自动删除, False:队列与交换机解绑后仍然保留交换机
            "internal": True             # True:仅允许创建交换机的程序分发信息, False:允许任意程序通过该交换机分发信息
        },

        # 队列设置
        "queueName": "testQueue",
        "queueOptions": {
            "passive": False,            # True:仅检查队列是否存在，False:若不存在则创建队列
            "durable": True,             # True:RMQ重启后保留队列(持久化), False:RMQ重启后删除队列
            "exclusive": False,          # True:只有创建队列的程序可以使用, False:所有连接都可以使用该队列
            "autoDelete": False          # True:没有消费者消费队列时自动删除, False:即便没有消费也保留队列
        },

        # 路由关键字
        "routingKey": "testKey"     # 交换机到队列的映射规则
    }