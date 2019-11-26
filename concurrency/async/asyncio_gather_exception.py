import asyncio
import random
from pprint import pprint


async def task_func(i):
    await asyncio.sleep(1)
    # 主动引发异常
    if random.randint(1,2) == 2:
        raise Exception("unexpected error")
    return "result(%d)" % i


async def main(num):
    tasks = [task_func(i) for i in range(num)]
    # 如果设置return_exception=True，asyncio.gather()会将出现的异常作为
    # 正常结果返回，有时候需要人为处理这些异常
    res = await asyncio.gather(*tasks, return_exceptions=True)
    res_ex_exception = [x for x in res if not isinstance(x, Exception)]

    print("exceptions in results: %d" % (len(res) - len(res_ex_exception),))
    return res_ex_exception


loop = asyncio.get_event_loop()
try:
    res = loop.run_until_complete(main(10))
finally:
    loop.close()

pprint(res)