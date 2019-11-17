"""
asyncio.wait()

asyncio.wait()将一系列协程作为输入，同时运行任务，并返回(completed,pending)。

completed和pending分别代表已完成和未完成任务，如果部分任务在完成前被取消，
则需要手动取消所有待定任务，否则程序会报错。
"""

import asyncio
import logging
import random
from pprint import pprint


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


async def fetch_url(i):
    try:
        logging.info("request url %d" % i)
        await asyncio.sleep(random.randint(1,3))
    except asyncio.CancelledError:
        print("cancel task: request url %d" % i)
    else:
        logging.info("get response from url %d" % i)
        return "result from url %d" % i


async def main(nums):
    fetchs = [fetch_url(i) for i in range(1,nums+1)]
    
    # asyncio.wait()将可等待对象(协程，Future，Task)的集合作为输入，返回元组(completed, pending)
    # completed代表已完成任务，pending表示正在等待的任务
    # 如果部分任务在完成前被取消，需要手动取消待定任务
    completed, pending = await asyncio.wait(fetchs, timeout=2)  # timeout=2, 任务在2秒内未完成直接取消
    logging.info("completed:%d  pending:%d" % (len(completed), len(pending)))
    
    # 取消待定任务
    if pending:
        logging.info("cancel all pending tasks")
        for t in pending:
            t.cancel()
    
    # 获取已完成任务的结果
    if completed:
        logging.info("retrieve results from completed tasks")
        results = [t.result() for t in completed]
        pprint(results)


loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(main(5))
finally:
    loop.close()

