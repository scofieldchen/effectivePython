"""
如何实现多线程间的通信？

一种简单有效的方法是使用队列(Queue)，假设部分线程负责'生产'数据，部分线程负责'消费'数据，Queue则充当数据中转站，
生产线程将数据存放在队列中，消费数据从队列中获取数据，为了避免冲突Queue自动实现了线程锁。
"""

import time
import random
import logging
from queue import Queue
from threading import Thread


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s-%(threadName)s-%(levelname)s-%(message)s"
)

# 负责'生产'数据的函数
def produce(q):
    while True:
        time.sleep(random.random())
        data = random.randint(1, 100)
        logging.info("produce number %d" % data)
        q.put(data)

# 负责'消费'数据的函数
def consume(q):
    while True:
        data = q.get()
        logging.info("consume number %d" % data)
        q.task_done()

# 创建一个共享的队列，启动两条线程，分别负责生产和消费
q = Queue()
t1 = Thread(target=produce, args=(q,), name="producer")
t2 = Thread(target=consume, args=(q,), name="consumer")
t1.start()
t2.start()