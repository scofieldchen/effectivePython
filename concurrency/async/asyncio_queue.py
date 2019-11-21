"""
asyncio.Queue

asyncio提供了队列(Queue)对象，实现协程间的通信，与queue.Queue对于线程和
multiprocessing.Queue对于进程的意义相同。

最经典的案例莫过于生产/消费模型。
"""

import asyncio
import random
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


async def producer(q):
    for i in range(10):
        # simulate i/o operation
        await asyncio.sleep(random.randint(1,2))
        item = "item(%d)" % i
        await q.put(item)
        logging.info("produce %s" % item)
    
    # indicate producing stop
    await q.put(None)


async def consumer(q):
    while True:
        item = await q.get()
        logging.info("consumer get %s" % item)
        
        if item is None:
            break


async def main():
    q = asyncio.Queue()
    await asyncio.gather(*(
        producer(q), consumer(q)
    ))


loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(main())
finally:
    loop.close()
