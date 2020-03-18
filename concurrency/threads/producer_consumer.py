"""
生产-消费模型

1. 多个生产者
2. 多个消费者
3. 通过队列交换数据
"""

import logging
import random
import time
from queue import Queue
from threading import Thread

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(threadName)s - %(message)s"
)


def producer(num, q):
    for _ in range(100):
        time.sleep(0.1)
        item = random.randint(1, 100)
        q.put(item)
        logging.info(f"producer{num} produce number {item}")
    
    q.put(None)  # 告诉消费者生产过程已经结束
    logging.info(f"producer{num} stop")


def consumer(num, q):
    while True:
        item = q.get()
        if item is None:  # 停止消费者
            break
        logging.info(f"consumer{num} get number {item}")
        q.task_done()
    
    logging.info(f"consumer{num} stop")


if __name__ == "__main__":

    q = Queue()

    producer_threads = [Thread(target=producer, args=(i, q), name="producer") for i in range(10)]
    consumer_threads = [Thread(target=consumer, args=(i, q), name="consumer") for i in range(5)]

    for ct in consumer_threads:
        ct.start()
    
    for pt in producer_threads:
        pt.start()

    for ct in consumer_threads:
        ct.join()

    for pt in producer_threads:
        pt.join()
