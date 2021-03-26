"""
Redis consumer group

## 什么是消费组？

消费组(consumer group): 消费组包含多个消费者，同时消费一个队列的消息，分别获得不同的消息。

假设某一个时刻有5条新消息，由一个消费组的3个消费者获得：

[item5, item4, item3, item2, item1] ==> [consumer1, consumer2, consumer3]

结果为：

* item1 -> consumer1
* item2 -> consumer2
* item3 -> consumer3
* item4 -> consumer1
* item5 -> consumer2

## 为什么使用消费组？

消费组的目标是实现负载均衡，当生产速度很快，但消费速度较慢时，可以使用消费组，多个消费者
分布在不同的线程中，加速消费的速度。

## 如何使用消费组？

1. 创建消费组(xgroup_create)
2. 在子线程启动消费者，监听消息(xreadgroup)
"""
import logging
import threading
import time
from typing import Any

import redis

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(threadName)s - %(message)s"
)


def producer(conn: redis.Redis, stream: str) -> None:
    while True:
        data = {"name": "value"}
        conn.xadd(stream, data)
        time.sleep(1)


def create_consumer_group(conn: redis.Redis,
                          stream: str,
                          group: str,
                          last_id: str = '$') -> None:
    # 先检查group是否存在，若存在则不创建，否则会引发异常
    groups = conn.xinfo_groups(stream)
    groups_names = [x["name"] for x in groups]

    if group not in groups_names:
        # 这里使用'$'作为ID，意味着该消费组仅接收最新消息，忽略历史消息
        # 如果使用0作为lastID, 则从历史第一条消息开始处理
        conn.xgroup_create(name=stream, groupname=group, id=last_id)
    else:
        print(f"Group '{group}' already exists!")


def consumer(conn: redis.Redis,
             stream: str,
             group: str,
             consumer: str,
             last_id: str = '>') -> None:
    while True:
        items = conn.xreadgroup(
            groupname=group,             # 消费组
            consumername=consumer,       # 子消费者
            streams={stream: last_id},   # '>'是特殊ID，表示从未发送给其它子消费者的最新消息，这往往是我们希望的结果，即不重复消费
            count=1,                     # 仅返回一条消息
            block=3000                   # 最多阻塞3秒
        )
        if items:
            # 提取每个消费者获取的消息ID，打印到控制台，跟其它消费者
            # 获取的消息ID比较，确保每个消费者获得不同的消息
            msg_id = _extract_id(items)
            logging.info(f"Receive message, id:{msg_id}")
        else:
            logging.info("No data coming in 3 seconds")


def _extract_id(items: Any) -> str:
    return items[0][1][0][0]


if __name__ == "__main__":
    r = redis.Redis(host="localhost", port=6379, decode_responses=True)

    stream = "test"  # stream name
    group = "mygroup"  # name of consumer group
    consumers = ["user1", "user2", "user3"]  # 消费组包含3个消费者

    thread_producer = threading.Thread(
        target=producer, args=(r, stream), name="producer")
    thread_producer.start()

    time.sleep(1)

    create_consumer_group(r, stream, group)
    thread_consumers = []
    for c in consumers:
        thread_consumers.append(threading.Thread(
            target=consumer,
            args=(r, stream, group, c),
            name=f"consumer-{c}"
        ))

    for t in thread_consumers:
        t.start()
