"""
Redis Stream作为消息队列
"""

import asyncio
import aioredis
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


async def consumer(stream, _id=0, host="localhost", port=6379, db=0):
    logging.info(f"Consumer({_id}) starts")
    conn_str = f"redis://{host}:{port}/{db}"
    redis = await aioredis.create_redis_pool(conn_str, encoding="utf8")
    while True:
        # xread()方法会阻塞直到获得消息
        # 返回list of tuples，每个元组包含3个元素：(stream, entryID, fields)
        data = await redis.xread([stream])
        if data:
            msg = dict(data[0][-1])
            logging.info(f"Consumer({_id}) recv: {str(msg)}")


async def main(stream, cnt=3):
    tasks = [consumer(stream, i) for i in range(cnt)]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    stream = "quote.00700"
    consumers = 1
    asyncio.run(main(stream, consumers))