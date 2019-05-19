import time
import logging
import random
import threading

"""
每一条线程都可以赋予名字，logging模块与线程完美兼容，只需定义'threadName'格式
就可以显示当前运行的线程的名字，方便debug.
"""

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(threadName)s - %(message)s"
)

def worker():
    cnt = 0
    while cnt < 20:
        logging.info("handle tasks")
        time.sleep(random.uniform(0.5, 2))
        cnt += 1

t1 = threading.Thread(target=worker, name="thread1")
t2 = threading.Thread(target=worker, name="thread2")

t1.start()
t2.start()

t1.join()
t2.join()
