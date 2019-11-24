"""
如何在事件环中运行同步函数？

为了实现并发，需要在子线程中运行同步函数，首先创建线程池，然后调用loop.run_in_executor()。

注意：要协调好同步函数(任务)的数量和线程池拥有的线程数量，1条线程在同一个时刻只会运行1个
同步函数，如果有1条子线程但有3个同步函数，仍然会按顺序执行，无法实现真正的并发。简答来说
线程的数量必须大于等于同步函数的数量。
"""

import asyncio
from concurrent.futures import ThreadPoolExecutor
import logging
import time

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(threadName)s - %(message)s"
)


# 创建同步函数，没有async,await
def block_func(i):
    logging.info("func(%d) starts" % i)
    time.sleep(1)
    logging.info("func(%d) ends" % i)


# 在线程池中运行同步函数，实现并发的目的
async def run_block_func(loop, executor, block_func_cnt):
    logging.info("create tasks")
    tasks = [loop.run_in_executor(executor, block_func, i) for i in range(block_func_cnt)]
    await asyncio.gather(*tasks)
    logging.info("all block funcs completed")


# 安排好同步函数和线程的数量，尝试变换两个参数，观察结果
block_func_cnt = 3
threads = 3

executor = ThreadPoolExecutor(max_workers=threads)
loop = asyncio.get_event_loop()

try:
    loop.run_until_complete(run_block_func(loop, executor, block_func_cnt))
finally:
    loop.close()