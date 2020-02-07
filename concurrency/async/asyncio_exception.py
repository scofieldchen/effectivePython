"""
如何在异步程序中处理异常？

1. 使用全局异常处理
2. 在任务内部使用try except
"""

import asyncio
import random
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


## 主动引发异常
# 如果不处理异常，程序会退出或卡住
# 如果用loop.run_until_complete()运行任务，遇到异常后会退出
# 如果用loop.run_forever()运行任务，遇到异常后先抛出'Task exception was never retrieved'，然后卡住 
# async def main():
#     while True:
#         logging.info("Doing some work")
#         await asyncio.sleep(random.randint(1, 2))
#         # 自动引发异常
#         if random.randint(1, 2) == 2:
#             raise Exception("Encounter exception")
#         await asyncio.sleep(1)

# # asyncio.run(main())
# loop = asyncio.get_event_loop()
# loop.create_task(main())
# loop.run_forever()


## 全局异常处理
# 创建异常处理函数，通过loop.set_exception_handler()添加到事件环
# def handle_exception(loop, context):
#     """函数必须接收loop, context两个参数"""
#     msg = context.get("exception", context["message"])
#     logging.error("Exception: %s" % msg)

# async def main():
#     while True:
#         logging.info("Doing some work")
#         await asyncio.sleep(random.randint(1, 2))
#         if random.randint(1, 2) == 2:
#             raise Exception("Encounter exception")

# loop = asyncio.get_event_loop()
# loop.set_exception_handler(handle_exception)
# try:
#     loop.run_until_complete(main())
# finally:
#     loop.close()


## try except
# 在异步程序中继续使用try except，比全局异常处理函数更加灵活
async def main():
    while True:
        try:
            logging.info("Doing some work")
            if random.randint(1, 2) == 2:
                raise Exception("Encounter exception")
        except Exception as e:
            logging.error(e)
        await asyncio.sleep(1)

asyncio.run(main())