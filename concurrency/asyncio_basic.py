import asyncio

async def run_task(x):
    print("start task %d" % x)
    await asyncio.sleep(1)  # 用sleep表示耗时任务
    print("task %d completed" % x)
    
async def main():
    await asyncio.gather(run_task(0), run_task(1))

asyncio.run(main())