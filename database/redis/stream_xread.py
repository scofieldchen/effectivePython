"""
Redis stream: 监听消息队列

command:
XREAD [COUNT count] [BLOCK milliseconds] STREAMS key id

xread可用于监听消息队列，适用于事件驱动型系统。
"""
import logging
import threading
import time
from pprint import pprint
from typing import Any, Dict, List

import redis

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(threadName)s - %(message)s"
)


def producer(conn: redis.Redis, stream: str) -> None:
    while True:
        data = {"user": "name"}
        conn.xadd(stream, data, maxlen=200)
        time.sleep(1)


def consumer(conn: redis.Redis,
             stream: str,
             block: int = 3000,
             count: int = 100) -> None:
    # xread监听队列要提供lastID, redis返回id大于等于lastID的所有消息
    # 第一次监听先使用特殊ID'$'作为lastID, '$'表示当前最大ID，即程序仅获取从现在开始的最新消息
    last_id = "$"
    streams = {stream: last_id}

    while True:
        # 阻塞block毫秒直到获取数据，最多返回count条消息
        # 若block毫秒内有数据到达，返回id >= lastID的消息
        # 若block毫秒后无数据到达，返回空列表
        # 若成功获取数据，更新lastID，这样才不会遗漏任何消息
        items = conn.xread(streams, block=block, count=count)
        if items:
            messages = _extract_messages(items)
            last_id = _extract_last_id(items)
            streams[stream] = last_id
            logging.info(f"Receive messages:{len(messages)}, lastID:{last_id}")
            # pprint(messages)
        else:
            logging.info(f"No data feed in 3 seconds, lastID:{last_id}")


def _extract_last_id(items: Any) -> str:
    return items[-1][-1][-1][0]


def _extract_messages(items: Any) -> List[Dict[str, Any]]:
    messages = items[0][1]
    return [msg[-1] for msg in messages]


if __name__ == "__main__":
    stream = "test"
    conn = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)
    
    thread_producer = threading.Thread(
        target=producer, args=(conn, stream), name="producer")
    
    thread_consumer = threading.Thread(
        target=consumer, args=(conn, stream), name="consumer")

    thread_consumer.start()
    thread_producer.start()
