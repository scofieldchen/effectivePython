"""
await or not to await ?

什么时候使用await？什么时候不使用await？这是是否真正实现并发的关键问题。

异步编程要求我们改变思维范式，考虑两个问题：1. 哪些任务需要按顺序执行，2. 哪些
任务能够即刻运行(fire and forget)。

如果一个任务必须按照多个步骤运行，例如first A, then B，B依赖于A的结果，这时必须使用
await A()，即等待A运行完毕，获取其结果后再运行B，就本质而言，这跟同步编程没有区别。

但如果A和B是非相互依赖的，就没有必要await，虽然await不会阻塞事件环，但它会阻塞B，
正确的做法是尽可能同时安排A和B作为事件环的任务，让它们尽快得到执行。
"""

import asyncio
import logging
import random

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


async def task_func(id):
    logging.info("run task %d" % id)
    await asyncio.sleep(random.randint(1,2))
    logging.info("complete task %d" % id)


## 假设任务必须按顺序执行
# async def main():
#     for i in range(10):
#         # 此处await不会阻塞事件环，但会阻塞task_func(i+1)，如果
#         # 第i个任务和第i+1个任务相互依赖，使用await是正确的选择
#         await task_func(i)

# loop = asyncio.get_event_loop()
# try:
#     loop.run_until_complete(main())
# finally:
#     loop.close()


## 假设任务相互独立，不需要await
## 如果希望单独安排任务，尽快执行，通常使用asyncio.create_task()
# async def main():
#     for i in range(10):
#         # 将单个任务提交给事件环，尽快执行，fire and forget
#         asyncio.create_task(task_func(i))

# loop = asyncio.get_event_loop()
# try:
#     # 注意这里的写法与上例不同，如果使用loop.run_until_complete(main())
#     # 事件环会在子任务完成前退出，引发异常
#     loop.create_task(main())
#     loop.run_forever()
# finally:
#     loop.close()


## 如果想同时执行相互独立的任务，使用asyncio.gather()
## gather()和create_task()的区别是，前者会收集批量任务，返回一个综合性的'Future'对象
## await gather()会等待所有任务完成，并按顺序返回结果，后者则直接将单个任务提交给
## 事件环，让任务在后台尽快执行。使用哪种方法取决于应用场景。 
async def main():
    tasks = [task_func(i) for i in range(10)]
    await asyncio.gather(*tasks)

loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(main())
finally:
    loop.close()