"""
asyncio.as_completed()

与gather()和wait()相似，as_completed()负责收集一系列任务，不同之处在于，
它每次只会返回一个已完成任务，最终返回结果的顺序是不确定的。
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
    results = []
    for next_to_complete in asyncio.as_completed(fetchs):
        res = await next_to_complete
        results.append(res)
    logging.info("all tasks completed")
    pprint(results)


loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(main(5))
finally:
    loop.close()

