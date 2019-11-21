import pika


# 建立连接
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

# 建立频道
channel = connection.channel()

# 声明队列，确保生产者的确创建了队列
channel.queue_declare(queue="test")

# 回调函数，处理message的逻辑
def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)

# channel.basic_consume(callback,
#                       queue="test",
#                       no_ack=True)

channel.basic_consume(
    queue="test", 
    on_message_callback=callback
)

print(' [*] Waiting for messages. To exit press CTRL+C')

channel.start_consuming()