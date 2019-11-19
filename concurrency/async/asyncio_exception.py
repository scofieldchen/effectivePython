"""
异步程序如何处理异常？
"""

import asyncio
import random
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


## 主动引发异常
## 如果不处理异常，系统会提示'Task exception was never retrieved'，程序也会卡住 
# async def fetch():
#     """模拟http请求，定时任务"""
#     while True:
#         logging.info("Send request")
#         await asyncio.sleep(random.randint(1, 2))
#         # 自动引发异常
#         if random.randint(1, 2) == 2:
#             raise Exception("Unexpected exception")
#         logging.info("Get response")
#         await asyncio.sleep(1)

# loop = asyncio.get_event_loop()
# try:
#     loop.create_task(fetch())
#     loop.run_forever()
# finally:
#     loop.close()


## 全局异常处理
## 创建异常处理函数，通过loop.set_exception_handler()添加到事件环
## 异常处理函数能够捕捉异常，但程序仍然会卡住？任务已经结束？
# def handle_exception(loop, context):
#     """函数必须接收loop, context两个参数"""
#     msg = context.get("exception", context["message"])
#     logging.error("Exception: %s" % msg)

# async def fetch():
#     """模拟http请求，定时任务"""
#     while True:
#         logging.info("Send request")
#         await asyncio.sleep(random.randint(1, 2))
#         # 自动引发异常
#         if random.randint(1, 2) == 2:
#             raise Exception("Unexpected exception")
#         logging.info("Get response")
#         await asyncio.sleep(1)

# loop = asyncio.get_event_loop()
# loop.set_exception_handler(handle_exception)  # 添加全局异常处理的逻辑
# try:
#     loop.create_task(fetch())
#     loop.run_forever()
# finally:
#     loop.close()


## try except
## 在异步程序中继续使用try except，捕捉异常后程序不会中断，比
## 全局异常处理函数更加灵活，也更容易理解
async def fetch():
    """模拟http请求，定时任务"""
    while True:
        try:
            logging.info("Send request")
            await asyncio.sleep(random.randint(1, 2))
            # 自动引发异常
            if random.randint(1, 2) == 2:
                raise Exception("Unexpected exception")
            logging.info("Get response")
            await asyncio.sleep(1)
        except Exception as e:
            logging.error(e)

loop = asyncio.get_event_loop()
try:
    loop.create_task(fetch())
    loop.run_forever()
finally:
    loop.close()