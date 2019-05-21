"""
程序有多个线程，如何实现线程间的通信和数据交互？

一种简单有效的办法是使用队列(Queue)，假设部分线程负责'生产'数据(获得数据流)，
部分线程负责'消费'数据(对流数据进行加工)，Queue充当数据中转站，生产线程将数据
存放在队列中，消费数据负责从队列中获得数据，为了避免冲突Queue自动实现了线程锁。

Queue教程：
https://pymotw.com/3/queue/index.html
"""

import time
import random
from queue import Queue
from threading import Thread


# 负责'生产'数据的函数
def produce(q):
    # q: 共享的队列实例
    while True:
        time.sleep(random.random())
        data = random.randint(1, 100)
        print("recieve number %d" % data)
        q.put(data)

# 负责'消费'数据的函数
def consume(q):
    # q: 共享的队列实例
    while True:
        data = q.get()
        print(data)
        q.task_done()

# 创建一个共享的队列实例，启动两条线程，分别负责生产和消费
q = Queue()
t1 = Thread(target=produce, args=(q,))
t2 = Thread(target=consume, args=(q,))
t1.start()
t2.start()