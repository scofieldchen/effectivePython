import pika


# 建立连接
connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))

# 创建频道
channel = connection.channel()

# 创建名为"test"的队列
channel.queue_declare(queue="test")

# 发送消息
msg = "hello world"
channel.basic_publish(
    exchange="",  # 交换机
    routing_key="test",  # 队列的名字
    body=msg  # 消息主体
)

print("send '%s'" % msg)

# 管理连接
connection.close()


