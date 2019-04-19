"""
多线程之间的通信非常复杂，python提供了简单的实现机制threading.Event,
多个线程可以一直等待某个事件发生，然后同时开始工作。

1个Event对象管理1个内部标识符(internal flag)，它取值True或False, 实例化
事件对象标识符默认为False。

Event对象有3个核心方法：
1. set ==> 将标识符设置为True
2. clear ==> 将标识符设置为False
3. wait ==> 阻碍线程直到标识符变为True
通过这3个方法实现多个线程之间的通信，可以理解为线程间的条件变量(if/then)。
"""

import time
from threading import Thread, Event
import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(threadName)s - %(message)s"
)


def worker(e):
    # e: threading.Event对象
    is_set = e.wait()
    logging.info("event is set: %s" % str(is_set))
    logging.info("doing work")


e = Event()

t = Thread(name="threadA", target=worker, args=(e,))
t.start()

time.sleep(10)
e.set()


