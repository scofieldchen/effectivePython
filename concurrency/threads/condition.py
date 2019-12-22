"""
线程同步机制：条件(Condition)

如何理解条件？

条件(Condition)是实现线程同步的一种机制，可以简单理解为在线程间实现if else逻辑。
假设两条线程A和B，线程A必须等待某个条件触发才会开始工作，线程B负责通知线程A这个
条件是否满足，一旦满足，线程A就会获取锁，排他性地对共享资源进行操作。

如何实现条件？

使用threading.Condition类。

Condition类提供四个核心接口：
1. acquire: Condition的实现基于Lock，一旦上锁，就获得共享资源的单独使用权。
2. release: 释放锁，其它线程可以尝试获取锁并修改共享资源。
3. wait: 将当前线程“挂起”，主动释放锁，直到被其它线程唤醒(条件得到满足)，如果
    在未获得锁前调用wait()，会引发异常。
4. notify: 唤醒其它线程，但不会主动释放锁，调用notify后需要使用release释放锁。

条件和锁的区别是什么？

条件在锁的基础上添加了逻辑判断。如果多条线程不仅会修改共享资源，还必须依赖某些
条件才能运行，就应该使用Condition类。

下面以简单的生产者-消费者模型作为案例

一条线程负责生产数据，另一条线程负责消费数据，两条线程必须在条件满足的情况下
才会运行：如果存储数据的媒介达到临界值，生产者停止生产，直到元素被消费者取出，
当存储数据的媒介没有任何元素，消费者暂停运行，直到生产者添加新的元素。
"""

import logging
import random
import time
from threading import Condition, Thread

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(threadName)s - %(message)s"
)

# 公共资源，生产者往里边添加元素，消费者消费元素，限定最多存储10个元素
items = []
condition = Condition()


class Producer(Thread):

    def __init__(self, condition, name="producer"):
        super().__init__(name=name)
        self._condition = condition

    def run(self):
        for _ in range(100):
            self.produce()
            time.sleep(2)

    def produce(self):
        global items
        self._condition.acquire()  # 获取锁
        if len(items) == 10:  # 缓存数据达到极限，生产者暂停生产
            logging.info("to many items, stop producing")
            self._condition.wait()  # 将‘生产’线程挂起，主动释放锁，直到被‘消费’线程唤起(notify)
            logging.info("resume producing")
        item = random.randint(100, 200)
        items.append(item)
        logging.info(f"produce number {item}, total items={len(items)}")
        self._condition.notify()  # 唤醒‘消费’线程，但不会主动释放锁
        self._condition.release()  # 释放锁


class Consumer(Thread):

    def __init__(self, condition, name="consumer"):
        super().__init__(name=name)
        self._condition = condition

    def run(self):
        for _ in range(100):
            self.consume()
            time.sleep(1)

    def consume(self):
        global items
        self._condition.acquire()  # 获取锁
        if len(items) == 0:
            logging.info("no item to consume, stop consuming")
            self._condition.wait()  # 将‘消费’线程挂起，主动释放锁，直到被‘生产’线程唤醒(notify)
            logging.info("notified by producer")
        item = items.pop(0)  # 模拟先进先出
        logging.info(f"consume number {item}, remaining items={len(items)}")
        self._condition.notify()  # 唤醒‘生产’线程
        self._condition.release()  # 主动释放锁


t1 = Producer(condition)
t2 = Consumer(condition)

t1.start()
t2.start()

t1.join()
t2.join()