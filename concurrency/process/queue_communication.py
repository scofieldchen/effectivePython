"""
如何在进程间交换数据？

两种方法：
1. 队列(queue)
2. 管道(pipe)

使用队列的原理与线程通信相似，但我们不使用queue.Queue对象，而是使用multiprocess.Queue对象，
后者是进程安全的。

继续使用经典的生产者-消费者模型解释如何用队列来通信。
"""

import time
import logging
import random
from multiprocessing import Process
from multiprocessing import Queue

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(processName)s - %(message)s"
)


class Producer(Process):
    """进程子类
    
    创建进程子类的步骤和线程类似：
    1. 重写构造方法，添加新的属性
    2. 重新run方法
    3. 实例化并调用start()，进而调用run()
    """
    def __init__(self, queue, name="producer"):
        super().__init__(name=name)
        self._queue = queue

    def run(self):
        for _ in range(10):
            item = random.randint(1, 100)
            self._queue.put(item)
            logging.info(f"Produce item {item}")
            time.sleep(random.randint(1, 3))
        
        self._queue.put(None)  # 告诉消费者生产已经结束
        logging.info("Stop producing")


class Consumer(Process):

    def __init__(self, queue, name="consumer"):
        super().__init__(name=name)
        self._queue = queue

    def run(self):
        while 1:
            item = self._queue.get()  # 阻塞进程直到获得元素
            if item is None:
                break
            logging.info(f"Consume item {item}")
            self._queue.task_done()
        
        logging.info("Stop consuming")


q = Queue()

producer = Producer(q)
consumer = Consumer(q)

producer.start()
consumer.start()

producer.join()
consumer.join()