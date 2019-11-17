"""
asyncio.wait()

wait()方法可以同时等待多个协程，让它们并发运行，最后获取所有结果。

案例：假设同时请求5个不同的url，可以同时发出请求，等待服务器响应，
然后收集所有结果。
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
    logging.info("request url %d" % i)
    await asyncio.sleep(random.randint(1,5))
    logging.info("get response from url %d" % i)
    return "result from url %d" % i


async def main(nums):
    fetchs = [fetch_url(i) for i in range(1,nums+1)]
    # asyncio.wait()将可等待对象(协程，Future，Task)的集合作为输入，返回一个元组(completed, pending)
    # completed代表已完成任务，pending表示正在等待的任务
    # await asyncio.wait()同时运行所有任务，然后不按顺序返回结果
    completed, _ = await asyncio.wait(fetchs)
    # completed.result()获取协程结果
    results = [t.result() for t in completed]
    logging.info("all fetchs are done")
    pprint(results)


loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(main(5))
finally:
    loop.close()

