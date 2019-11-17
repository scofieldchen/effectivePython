import asyncio


async def task_func():
    """假设任务耗时2秒"""
    print("task running")
    await asyncio.sleep(2)
    print("task completed")
    return "result"


async def cancel_task(t):
    """在任务完成前取消"""
    await asyncio.sleep(1)
    print("cancel task")
    t.cancel()
    print("task cancelled")


async def main(loop):
    print("create task")
    t = loop.create_task(task_func())
    try:
        # gather(*coro)收集task_func和cancel_task两个协程对象，让它们同时运行
        # 结果是在任务没有完成前就被取消，这时候会引发CancelledError异常
        await asyncio.gather(*(t, cancel_task(t)))
    except asyncio.CancelledError:
        pass


loop = asyncio.get_event_loop()
try:
    res = loop.run_until_complete(main(loop))
finally:
    loop.close()