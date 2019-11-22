import time
from json import loads

from kafka import KafkaConsumer


# 创建消费者实例(迭代器)
consumer = KafkaConsumer(
    "test",  # topic name, 自动创建topic
    bootstrap_servers=["localhost:9092"],  # kafka集群
    auto_offset_reset="latest",  # 从哪里重新读取消息，'latest' or 'earliest', 前者读取最新数据，后者从断开的位置读取
    group_id="myGroup",  # 属于哪个消费群
    value_deserializer=lambda x:loads(x.decode("utf-8"))  # 去序列化
)

for msg in consumer:
    print("%s:%d:%d: key=%s value=%s" % (
        msg.topic, msg.partition, msg.offset,
        msg.key, msg.value
    ))
