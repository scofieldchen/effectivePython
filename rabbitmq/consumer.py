import pika


class Consumer:

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

    def __enter__(self):
        self.connection = self._create_connection()
        return self

    def __exit__(self, *args):
        self.connection.close()

    def _create_exchange(self, channel):
        exchange_options = self.config["exchangeOptions"]
        channel.exchange_declare(
            exchange=self.config["exchangeName"],
            exchange_type=self.config["exchangeType"],
            passive=exchange_options["passive"],  # bool, True:检查交换机是否存在, False:令RMQ创建交换机
            durable=exchange_options["durable"],  # bool, True:RMQ重启后保留交换机, False:RMQ重启后删除交换机
            auto_delete=exchange_options["autoDelete"],  # bool, True:当所有队列与交换机解绑后自动删除交换机, False:所有队列与交换机解绑后仍然保留交换机
            internal=exchange_options["internal"]  # bool, True:仅允许创建该交换机的程序生产信息, False:允许任意程序通过该交换机生产信息
        )
