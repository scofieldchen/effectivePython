"""
asyncio.gather()

asyncio.gather(*coro)用于收集一系列任务，并按顺序返回结果。

gather()和wait()是收集任务的两个高级接口，与wait()不同，gather()
不返回已完成或待定任务对象，所以无法取消任务，但不管哪个任务先完成，
它都会按照顺序返回结果。

gather()返回“综合”的Future对象，当使用await asyncio.gather(*coro),
事件环会等待所有任务都完成并返回结果。
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
    results = await asyncio.gather(*fetchs)
    logging.info("all fetchs are done")
    pprint(results)


loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(main(5))
finally:
    loop.close()

