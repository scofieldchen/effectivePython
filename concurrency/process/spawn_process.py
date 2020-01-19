"""
用multiprocessing生成和启动子进程

专用术语：Spawn，父进程创建/生成子进程。

步骤：
1. 定义worker函数，负责具体工作。
2. 创建Process对象。
3. 调用进程对象的start()方法。
4. 调用进程对象的join()方法，如果不调用，子进程会持续运行，即便工作已经完成也不会退出。
"""

import multiprocessing
import logging
import time

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(processName)s - %(message)s"
)


# 定义目标函数
def worker():
    logging.info("doing some work")
    time.sleep(3)


process_jobs = [multiprocessing.Process(target=worker, name=f"Process{i}") for i in range(5)]

# start和join方法的调用过程必需要分开，先调用全部进程的start()，再调用join()
# 否则无法实现并行
for job in process_jobs:
    job.start()

for job in process_jobs:
    job.join()

logging.info("All processes completed")