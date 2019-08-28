"""
异步初步

https://realpython.com/async-io-python/
"""

import time
import asyncio
import random


## 异步IO简介

# 平行运算：同时使用多个CPU核进行运算
# 协程：在同一个CPU中同时运行多个任务
# 异步IO(asyncioIO)属于协程运算，与threading非常相似

## asyncio, async/await

# async def count():
#     print("one")
#     await asyncio.sleep(1)
#     print("two")

# async def main():
#     await asyncio.gather(count(), count(), count())

# t0 = time.time()
# asyncio.run(main())
# elapsed = time.time() - t0
# print("finished in %.2f seconds" % elapsed)

# async def定义异步函数，内置异步处理机制，一个异步函数就是一个协程(coroutine)，在asyncio中
# 由一个统一的事件环(event loop)来处理，await把异步函数的主动权交还给事件环，先让其它的协程
# 运行，得到相关的返回结果后再继续运行
# 如果在函数g()内部定义await f()，相当于告诉事件环，先把g()的控制权交给事件环，等到f()运行完毕
# 后再继续g()的运行

# async/await的使用规则

# async def ==> 定义异步函数/协程，内置异步处理机制，可在内部使用await,return,yield，为了调用异步函数，必须'等待(await)'并得到它的结果
# await必须在异步函数内调用，在函数外/或非异步函数内调用是非法的
# 所有异步函数都是可等待对象(awaitable object)

# 1. async def ==> 定义异步函数/协程
# 2. asyncio.gather ==> 收集任务(大量协程)，创建一个中央协程管理众多子协程，类似于创建线程池/进程池
# 3. asyncio.run ==> 创建事件环开始运行/管理所有协程，直到完成所有任务

async def make_random_num(i, threshold):
    """生成0-10之间的随机数，直到超过threshold为止"""
    num = random.randint(0, 10)
    while num <= threshold:
        print("asyncio %d: random integer = %d" % (i, num))
        await asyncio.sleep(1)
        num = random.randint(0, 10)
    print("asyncio %d: task done, num = %d" % (i, num))
    return num

async def main():
    res = await asyncio.gather(*(make_random_num(i, 8) for i in range(3)))
    return res

r1, r2, r3 = asyncio.run(main())
print("r1:%d, r2:%d, r3:%d" % (r1,r2,r3))

## 异步IO的设计模式

## 异步IO和生成器的联系

## 案例分析：异步请求

## 何时使用异步IO最合适