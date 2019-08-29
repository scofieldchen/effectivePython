"""
假设多个线程要同时修改公共资源，很有可能导致‘数据赛跑(race condition)’，为了
避免冲突，需要使用锁(threading.Lock)，所谓‘锁’其实就是绑定公共资源的变量，锁
有两个状态：‘上锁(locked)’和‘解锁(unlocked)’，当一个锁在一条线程中被锁定，
其它线程将不能再获得该锁直到锁被释放，这样就能保证多条线程完全互斥。
"""

import time
import random
import logging
from threading import Thread, Lock


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(threadName)s - %(levelname)s - %(message)s"
)


class Counter:

    def __init__(self, value=0):
        self.value = value
        self.lock = Lock()
    
    def increment(self):
        self.lock.acquire()  # 将锁的状态变为'locked'，其它线程将无法再调用acquire
        logging.info("acquire lock")
        self.value += 1  # 锁机制保证在同一个时刻只有一条线程在修改公共资源
        logging.info("increment counter, value = %d" % self.value)
        self.lock.release()  # 将锁的状态变为'unlocked'，其它线程可以调用acquire
        logging.info("release lock")


def worker(n, counter):
    while n > 0:
        time.sleep(random.random())
        counter.increment()
        n -= 1


counter = Counter(0)  # 公共资源

threads = []
for i in range(2):
    t = Thread(target=worker, args=(10, counter), name="thread(%d)" % (i+1))
    threads.append(t)

for t in threads:
    t.start()

for t in threads:
    t.join()
