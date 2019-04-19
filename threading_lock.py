"""
threading.Lock
"""

import time
import random
import threading
import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(threadName)s - %(message)s"
)


"""
创建全局变量l(list)，启动子线程，不断往里边增加数字，
主线程则负责计算l中数字之和。
"""

l = []

def worker(l):
    for _ in range(100):
        time.sleep(random.random())
        l.append(1)
        logging.info(str(l))

if __name__ == "__main__":
    
    t = threading.Thread(name="child", target=worker, args=(l,))
    t.start()
    
    lock = threading.Lock()
    for _ in range(100):
        time.sleep(random.random())
        try:
            lock.acquire()
            logging.info("lock acquired")
            logging.info("sum = %d" % sum(l))
        finally:
            lock.release()
            logging.info("release lock")

