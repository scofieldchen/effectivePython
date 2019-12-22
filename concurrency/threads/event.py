"""
线程同步机制：事件(Event)

如何理解事件？

事件是实现线程同步的一种机制，一个线程负责设置事件的状态，发生或未发生，其余多个
线程等待(阻塞)，直到事件发生。

如何实现事件？

使用threading.Event类

Event类管理一个内部标识符，有两种状态：True或者False，True表示事件已发生，等待
的线程开始工作，False表示事件未发生，其余线程将阻塞直到事件发生。

Event类提供3个核心接口：
1. wait() ==> 阻塞线程直到事件被设置
2. set() ==> 设置事件，内部标识符变为True
3. clear() ==> 清除设置，内部标识符变为False

事件和锁，条件的区别是什么？

案例：1个线程负责周期性的设置/清除事件，另外一个线程在事件发生时开始工作。
"""

from threading import Thread, Event
import logging
import time


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(threadName)s - %(message)s"
)


class ControlThread(Thread):

    def __init__(self, event, name="control"):
        super().__init__(name=name)
        self._event = event

    def run(self):
        for _ in range(20):
            time.sleep(5)
            self._event.clear()  # 将事件的状态设置为False
            logging.info("stop other threads, wait 5 seconds")
            time.sleep(5)
            self._event.set()  # 设置事件，启动其余等待的线程
            logging.info("event has been set")


class WorkerThread(Thread):

    def __init__(self, event, name="worker"):
        super().__init__(name=name)
        self._event = event

    def run(self):
        while True:
            time.sleep(1)
            self._event.wait()  # 如果事件未发生，阻塞线程
            logging.info("doing some work")


e = Event()

ct = ControlThread(e)
wt = WorkerThread(e)

ct.start()
wt.start()

ct.join()
wt.join()

