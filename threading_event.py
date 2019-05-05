import time
import random
import logging
from threading import Thread, Event


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(threadName)s - %(message)s"
)


def trading():
    while True:
        pause = random.randint(5, 10)
        time.sleep(pause)
        logging.info("wait for monitor to finish")
        e_monitor.wait()  # 阻碍该线程直到monitor结束
        logging.info("monitor is over")
        e_trade.clear()
        logging.info("place orders randomly")
        e_trade.set()


def depth():
    while True:
        pause = random.randint(2, 5)
        time.sleep(pause)
        logging.info("wait for monitor to finish")
        e_monitor.wait()  # 阻碍该线程直到monitor结束
        logging.info("monitor is over")
        e_depth.clear()
        logging.info("place and cancel limit orders")
        e_depth.set()


def monitor():
    while True:
        time.sleep(1)
        e_trade.wait()
        e_depth.wait()
        logging.info("trade and depth not running")
        e_monitor.clear()
        logging.info("monitor order flow")
        e_monitor.set()


if __name__ == "__main__":

    e_trade = Event()
    e_depth = Event()
    e_monitor = Event()

    e_trade.set()
    e_depth.set()
    e_monitor.set()

    t1 = Thread(name="trade", target=trading)
    t2 = Thread(name="depth", target=depth)
    t3 = Thread(name="monitor", target=monitor)

    t1.start()
    t2.start()
    t3.start()
