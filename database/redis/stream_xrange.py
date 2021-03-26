"""
Redis stream xrange/xrevrange

由于stream中每条消息都有entryID, entryID由时间戳构成，所以可将stream视为时序数据库，
通过xrange/xrevrange可迭代所有消息，适用于创建流处理应用。

案例分析：聚合多个交易所的实时报价。

1. 监听多个交易所多个品种的实时报价。
2. 生产者先把所有报价推送到一条stream.
3. 消费者从stream中批量提取数据。
4. 消费程序对数据进行实时聚合。
5. 将聚合数据推送到其它应用。
"""
import logging
import random
import threading
import time
from typing import Any, Dict, List, Tuple

import redis

# 模拟3个交易所和3种货币对
EXCHANGES = ["huobi", "binance", "okex"]
SYMBOLS = ["btcusdt", "ethusdt", "ltcusdt"]

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(threadName)s - %(levelname)s - %(message)s"
)


def simulate_tick() -> Dict[str, Any]:
    """模拟交易所推送的实时报价"""
    return {
        "exchange": random.sample(EXCHANGES, 1)[0],
        "symbol": random.sample(SYMBOLS, 1)[0],
        "price": round(random.random(), 4),
        "timestamp": int(time.time() * 1000)
    }


def producer(conn: redis.Redis,
             stream: str,
             interval: Tuple[int, int]) -> None:
    """快速生成tick报价，发送到redis stream"""
    while True:
        try:
            tick = simulate_tick()
            conn.xadd(stream, tick)
        except Exception as e:
            logging.error(e)
        interval_sec = random.randint(interval[0], interval[1]) / 1000
        time.sleep(interval_sec)


def consumer(conn: redis.Redis,
             stream: str,
             time_window: int = 1,
             max_items: int = 1000) -> None:
    """从redis stream批量获取实时报价，然后聚合价格
    
    xrange key start end count -> 返回ID处于[start, end]的前count条消息

    1. 以某个时间为起点，获取最多n条消息
    2. 批处理数据，如聚合价格
    3. 记录返回消息中的最大ID，作为下一轮查询的起始时间
    4. 暂停k秒
    5. 回到第一步
    """
    # 以当前时间作为第一次查询的起始时间
    # 结束时间固定使用'+'，这是特殊ID，表示队列中所有消息的最大ID
    start_id = str(int(time.time() * 1000)) + "-0"  # '-0'为sequenceNumber, 可忽略
    end_id = "+"

    while True:
        try:
            # 先等待消息入队
            time.sleep(time_window)

            # 最多获取max_items条消息
            items = conn.xrange(
                stream, min=start_id, max=end_id, count=max_items)
            
            if items:
                messages = _extract_messages(items)
                # 获取返回消息中的最大ID，作为下一轮查询的起点
                # 在ID左边添加'('，这是特殊ID，表示获取大于但不包含该条ID的最新消息
                # 这样就可以保证每条消息仅消费一次
                last_id = _extract_last_id(items)
                start_id = "(" + last_id
                logging.info(f"Receive messages:{len(messages)}, lastID:{last_id}")
            else:
                logging.info(f"No data coming in {time_window} seconds")
        except Exception as e:
            logging.error(e)


def _extract_messages(items: Any) -> List[Dict[str, Any]]:
    return [item[1] for item in items]


def _extract_last_id(items: Any) -> str:
    return items[-1][0]


def _evaluate_elapsed_time(last_id: str) -> float:
    now = int(time.time() * 1000)
    last_ts = int(last_id.split("-")[0])
    return now - last_ts


if __name__ == "__main__":
    interval = (10, 20)  # 消费者生产数据的随机时间间隔，毫秒
    stream = "test"
    time_window = 1  # 每个1秒批量获取历史数据
    max_items = 1000  # 每次最多处理1000条消息
    
    conn = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)
    
    thread_producer = threading.Thread(
        target=producer, args=(conn, stream, interval), name="producer")
    
    thread_consumer = threading.Thread(
        target=consumer, args=(conn, stream, time_window, max_items), name="consumer")
    
    thread_consumer.start()
    thread_producer.start()
