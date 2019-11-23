"""
为了正常关闭异步程序，需要添加额外的逻辑，主要包含两点：
1. 清理资源，例如数据库连接，文件连接等。
2. 取消pending任务。

如何取消任务？

1. 获取pending tasks
2. 调用task.cancel()，注意这不会立即“取消”任务，甚至不能保证任务被取消，调用cancel()
   的真正含义是在下一轮循环中取消任务，所以要先等待它们完成。
3. task.cancel()会引发CancelledError异常，是否需要处理？如何处理异常？
"""

import asyncio
import logging
import signal

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


async def task_func(i):
    # while True:
    #     logging.info("task_func(%d) starts" % i)
    #     await asyncio.sleep(1)
    #     logging.info("task_func(%d) stops" % i)

    try:
        while True:
            logging.info("task_func(%d) starts" % i)
            await asyncio.sleep(1)
            logging.info("task_func(%d) stops" % i)
    except asyncio.CancelledError:
        pass

async def shutdown(signal, loop):
    logging.info("Received exit signal %s" % signal.name)
    # 关闭整个程序前最好先清理资源，如果没有必要直接跳过
    logging.info("Clean up resources, like database connection")

    # 取消任务：先获取pending tasks，调用task.cancel()发送取消请求，等待任务完成
    # 这样就能(不完全保证)在下一轮循环中终止任务
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
    [task.cancel() for task in tasks]
    logging.info("Cancelling %d pending tasks" % len(tasks))
    # task.cancel()会引发CancelledError异常，这个异常必须得到处理，否则整个程序会卡住！！！
    # 有两种处理异常的方式：
    # 第一：被取消的任务由asyncio.gather()安排，则使用gather()时设置return_exceptions=True, 将异常以正常结果返回(忽略异常)
    # 第二：在被取消的任务(此处是task_func)内部使用try except，明确捕捉CancelledError，并忽略它
    await asyncio.gather(*tasks)

    # 取消任务后记得停止事件环
    loop.stop()


loop = asyncio.get_event_loop()

signals = (signal.SIGHUP, signal.SIGTERM, signal.SIGINT)
for s in signals:
    loop.add_signal_handler(
        s, lambda s=s: asyncio.create_task(shutdown(s, loop))
    )

try:
    for i in range(10):
        loop.create_task(task_func(i))
    loop.run_forever()
finally:
    loop.close()
    logging.info("Shutdown successfully")