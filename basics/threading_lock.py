"""
threading.Lock
"""

import time
import threading
import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(threadName)s - %(message)s"
)


class Counter:
    def __init__(self):
        self.value = 0
    
    def increment(self, offset):
        self.value += offset


def worker(how_many, counter):
    for _ in range(how_many):
        logging.info("counter = %d" % counter.value)
        counter.increment(1)


def run_threads(how_many, counter):
    threads = []
    for i in range(5):
        t = threading.Thread(name="thread%d" % i, target=worker, 
                             args=(how_many, counter))
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()


counter = Counter()
how_many = 500000
run_threads(how_many, counter)


