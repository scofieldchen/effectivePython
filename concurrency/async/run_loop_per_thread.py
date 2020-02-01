"""
在子线程中运行事件环

1. 调用asyncio.new_event_loop()创建新事件环
2. 在子线程中调用asyncio.set_event_loop(loop)为该子线程设置事件环
3. 运行子线程
"""

import asyncio
import logging
import time
from threading import Thread

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(threadName)s - %(levelname)s - %(message)s"
)


class ThreadLoop:
    def __init__(self):
        self._running = True

    def terminate(self):
        self._running = False

    def run(self, loop):
        # 为子线程设置事件环
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.task_func())
        loop.close()

    async def task_func(self):
        while self._running:
            logging.info("Doing some work")
            await asyncio.sleep(1)


if __name__ == "__main__":

    # 创建新事件环
    new_loop = asyncio.new_event_loop()

    thread_loop = ThreadLoop()

    t = Thread(target=thread_loop.run, args=(new_loop,))
    logging.info("Run event loop in child thread")
    t.start()

    time.sleep(10)

    logging.info("Terminate thread")
    thread_loop.terminate()
    t.join()