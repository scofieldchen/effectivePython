"""
Redis Stream作为消息队列
"""

import asyncio
import aioredis
import random
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


async def connect(host="localhost", port=6379, db=0):
    conn_str = f"redis://{host}:{port}/{db}"
    return await aioredis.create_redis_pool(conn_str)


async def producer(redis, stream, max_len=300, interval=1):
    while True:
        data = {
            "bid": random.randint(1, 10),
            "ask": random.randint(11, 20)
        }
        await redis.xadd(stream, data, max_len=max_len)
        logging.info(f"Producer send msg {str(data)}")
        await asyncio.sleep(interval)


async def check_items(redis, stream, interval=1):
    while True:
        items = await redis.xlen(stream)
        logging.info(f"Length of {stream}: {items}")
        await asyncio.sleep(interval)


async def main():
    redis = await connect()
    stream = "test"
    tasks = [
        producer(redis, stream, 300, 0.1),
        check_items(redis, stream, 1)
    ]
    await asyncio.gather(*tasks)
    

if __name__ == "__main__":
    asyncio.run(main())