"""
chained coroutine: 将协程连接在一起

尽管协程函数可以'并发'运行，但部分协程仍然有执行的顺序，例如协程B要获得
协程A的结果，协程C要获得协程B的结果，这时候就需要使用'chained coroutine'
"""

import asyncio
import random
import time


async def step1():
    print("execute step1")
    pause = random.randint(1,3)
    await asyncio.sleep(pause)
    print("step1 completed in %.2f seconds" % pause)


async def step2():
    print("execute step2")
    pause = random.randint(1,4)
    await asyncio.sleep(pause)
    print("step2 completed in %.2f seconds" % pause)


async def step3():
    print("execute step3")
    pause = random.randint(2,4)
    await asyncio.sleep(pause)
    print("step1 completed in %.2f seconds" % pause)


async def complete_task():
    """将step1,step2,step3连接在一起"""
    t0 = time.time()
    await step1()  # 等待第一步执行完毕
    await step2()  # 等待第二步执行完毕
    await step3()  # 等待第三步执行完毕
    print("tasks completed in %.2f seconds" % (time.time() - t0))


loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(complete_task())
finally:
    loop.close()