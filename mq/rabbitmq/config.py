# RabbitMQ配置
RABBIT = {
    # 身份认证
    "username": "guest",
    "password": "guest",
    
    # 连接参数
    "host": "localhost",             # 终端
    "port": 5672,                    # 端口，默认5672
    "virtualHost": "/",              # 虚拟机，username=guest使用默认虚拟机'/'
    
    # 交换机设置
    "exchangeName": "testExchange",  # 交换机名称
    "exchangeType": "direct",        # 交换机类型，'fanout','direct','topic'
    "exchangeOptions": {
        "passive": False,            # True:仅检查交换机是否存在, False:若不存在则创建交换机
        "durable": True,             # True:RMQ重启后保留交换机(持久化), False:RMQ重启后删除交换机
        "autoDelete": False,         # True:当所有队列与交换机解绑后自动删除, False:队列与交换机解绑后仍然保留交换机
        "internal": False            # True:仅允许创建交换机的程序分发信息, False:允许任意程序通过该交换机分发信息
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
    "routingKey": "testKey"          # 交换机到队列的映射规则
}


# mongodb配置
MONGODB = {
    "host": "localhost",
    "port": 27017,
    "db": "marketmaking",
    "collection": "robots"
}