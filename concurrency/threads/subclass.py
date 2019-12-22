"""
继承threading.Thread类，创建线程子类，需要重写构造方法和run()方法。
"""

import logging
import threading
import time

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(threadName)s - %(message)s"
)


class MyThread(threading.Thread):

    def __init__(self, name, loops=5, interval=1):
        super().__init__(name=name)
        self.loops = loops
        self.interval = interval

    def run(self):
        """必须重写run方法，调用start会调用run"""
        logging.info(f"{self.name} starts")
        
        while self.loops > 0:
            logging.info(f"{self.name} is working")
            self.loops -= 1
            time.sleep(self.interval)
        
        logging.info(f"{self.name} exits")


t1 = MyThread("threadA", 5, 1)
t2 = MyThread("threadB", 10, 1)

t1.start()
t2.start()

logging.info("Main thread")
time.sleep(2)

t1.join()
t2.join()