"""
定义线程

在Python中，使用threading模块管理线程。

1. 创建threading.Thread实例，提供目标函数，函数将在子线程中执行。
2. 调用start()方法，启动子线程。
3. 调用join()方法，等待子线程运行完毕并回归主线程。
"""

import time
from threading import Thread
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(threadName)s - %(levelname)s - %(message)s"
)


# 定义worker函数
def simple_worker(i):
    for _ in range(10):
        logging.info(f"worker({i}) is running")
        time.sleep(1)


# 定义多个线程
threads = []
for i in range(5):
    t = Thread(
        target=simple_worker,  # 目标函数
        name="thread(%d)" % i,  # 线程名称，默认为'Thread-N'
        args=(i,)  # 提供给目标函数的参数，必须提供一个元组 
    )
    threads.append(t)


# 启动线程
for t in threads:
    t.start()

# 调用t.join()会阻塞主线程，直到子线程运行完毕并回归主线程
for t in threads:
    t.join()


logging.info("All child threads completed")