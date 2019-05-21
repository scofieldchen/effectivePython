"""
Thread对象有一个属性daemon，可以设置为True或False:
若daemon = True: 主进程退出时会同时关闭子进程，不管子进程是否运行完毕
若daemon = False: 主进程退出时会先检测子进程是否已经结束，如果没有
则等待它运行完毕后再退出。

为什么使用daemon thread?

有时候子进程负责爬取数据，例如通过Websocket API获得实时数据，然后在主进程
中进行计算，当主进程结束时就不再需要这些数据，同时关闭子进程会更好，这时就
可以将daemon属性设置为True。
"""

import time
import threading
import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(threadName)s - %(message)s"
)


def daemon():
    """
    daemon thread的worker函数，假设主进程在1秒后停止，
    该子线程也会停止，"thread ends"不会出现
    """
    logging.info("thread starts")
    time.sleep(2)
    logging.info("thread ends")


if __name__ == "__main__":

    t = threading.Thread(target=daemon, name="daemon", daemon=True)
    t.start()
    time.sleep(1)
    #t.join()  # 如果调用join方法，则无法如何主进程都会等待子进程结束再退出

