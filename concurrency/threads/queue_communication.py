"""
线程通信机制：队列(queue)

如何理解队列？

队列充当数据中转站，在不同的线程间共享数据。队列的实现基于锁，防止竞态条件。

队列的作用类似于工厂的传送带，一个车间生产产品，通过传送带将其送到其它车间进行
加工。在经典的生产者-消费者模型中，部分线程充当生产者，将元素放入队列，部分线程
是消费者，从队列中取出元素后进行加工处理。

如何用队列实现通信？

使用queue.Queue类。

Queue类提供四个核心接口：
1. put() ==> 将元素放入队列，存入数据前先获取锁。如果队列已满，使用block参数
    决定是否阻塞，block=True会阻塞直到有空插槽，False会引发Full异常。
2. get() ==> 从队列中取出元素，取出数据前先获取锁，如果队列为空，使用block参数
    决定是否阻塞，block=True会阻塞直到有元素可消费，False会引发Empty异常。
3. task_done() ==> 表示前面排队的任务已经完成。
4. join() ==> 阻塞直到队列中的所有元素被接收和处理完成。Queue会记录未完成任务
    的计数，当调用put()将元素放入队列，未完成任务的计数会增加，相反当调用get()
    获取元素并调用task_done()，未完成任务的计数会减少。当调用join()方法阻塞主
    线程时，未完成任务的计数归零就会解除阻塞。

队列与锁，条件，事件的区别是什么？

锁，条件，事件等机制解决线程同步问题，避免同时修改共享资源；队列解决线程通信的
问题，在不同线程间共享数据。

案例：经典的生产者-消费者模型。
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


def producer(q):
    for _ in range(10):
        time.sleep(1)
        item = random.randint(1, 100)
        q.put(item)
        logging.info(f"put item {item} into queue")
    
    q.put(None)  # 告诉消费者生产过程已经结束
    logging.info("producer stop")


def consumer(q):
    while True:
        item = q.get()
        if item is None:  # 停止消费者
            break
        logging.info(f"get item {item} from queue")
        logging.info("do some work on item")
        q.task_done()
    
    logging.info("consumer stop")


q = Queue()

t1 = Thread(target=producer, args=(q,), name="producer")
t2 = Thread(target=consumer, args=(q,), name="consumer")

t1.start()
t2.start()

t1.join()
t2.join()
