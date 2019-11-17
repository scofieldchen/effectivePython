"""
创建并启动任务(Task)

Task可理解为很多协程的集合，只要将任务提交给事件环，后者会正确执行所有
子协程，并返回结果。

案例：假设我们要请求某网站API，创建一个请求任务，分为两个子过程：1. 请求
服务器，等待响应；2. 解析结果。
"""

import asyncio


async def fetch_url():
    """请求任务，将两个协程链接在一起"""
    resp = await request()
    parsed = await parse(resp)
    return parsed


async def request():
    print("send request to server")
    await asyncio.sleep(1)
    print("get response from server")
    return {"status": 200, "resp": "html contents"}


async def parse(resp):
    print("parse response")
    return resp["resp"]


async def main(loop):
    # loop.create_task()创建任务，并返回Task对象
    task = loop.create_task(fetch_url())
    print("create task %s" % str(task))
    res = await task  # 等待任务完成，获取结果
    return res


loop = asyncio.get_event_loop()
try:
    res = loop.run_until_complete(main(loop))
    print("task result: %s" % res)
finally:
    loop.close()