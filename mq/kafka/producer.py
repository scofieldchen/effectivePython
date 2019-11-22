import time
from json import dumps

from kafka import KafkaProducer


# 创建生产者实例
producer = KafkaProducer(
    bootstrap_servers=["localhost:9092"],
    value_serializer=lambda x:dumps(x).encode("utf-8")  # 在发送至broker前序列化
)

for i in range(10):
    msg = {"number": i}
    producer.send("test", value=msg)
    time.sleep(2)