"""
创建和启动协程
"""

import asyncio


async def coro():
    print("do some work")
    await asyncio.sleep(2)
    return "result"


loop = asyncio.get_event_loop()
try:
    # run_until_complete是最简单的运行协程的方法，适用一次性任务，
    # 并返回协程函数的结果，如果协程函数不返回，run_until_complete返回None
    res = loop.run_until_complete(coro())
finally:
    loop.close()
    print("coro function returns: %s" % str(res))