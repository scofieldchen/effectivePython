"""
Redis Streams: 实现消息队列的数据结构

streams的特点：

1. 数据存储：name: [{key:value}, {key:value}, ...]
2. 每条消息都有entryID, 格式为'<timestamp>-<sequenceNumber>', redis默认使用
    入队时间戳作为ID，意味着stream也可以作为时序数据库
3. 广播消息(fan-out)，即多个消费者可同时监听同一个队列，并获得相同的消息
4. 数据会持久化在内存中，直到用户主动删除历史记录
5. 支持消费者组，实现负载均衡
"""
from pprint import pprint

import redis


################################ 建立连接 ################################

r = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)
stream = "test"

################################ 插入数据 ################################

# XADD key ID field value [field value]
r.xadd(
    name=stream,
    fields={
        "username": "kobe",
        "password": "123",
        "age": 25
    }
)

# 查询stream长度
print(r.xlen(stream))

################################ 范围查询 ################################

# 范围查询：xrange
# XRANGE key START END COUNT --> 返回ID处于[START, END]范围的前COUNT条消息
# '-'表示最小ID(最旧消息的ID)，'+'表示最大ID(最新消息的ID)
# count为可选参数，若不提供返回所有消息
pprint(r.xrange(stream, min="-", max="+", count=10000))

# 范围查询：xrevrange
# 功能跟xrange相同，但时间戳按从大到小的顺序返回数据，第一条数据为最新数据
# XREVRANGE key END START COUNT --> 返回ID处于[END, START]范围的前COUNT条消息
pprint(r.xrevrange(stream, max="+", min="-", count=10000))

################################ 监听队列 ################################

# 监听队列：xread
# XREAD [COUNT count] [BLOCK milliseconds] STREAMS key ID
# xread的工作原理和xrange完全不同，前者负责监听队列，接收最新消息，通常用于事件驱动型应用，
#   后者将stream视为时序数据库，用于批处理应用(stream processing)
# count和block都是可选参数，重点在于理解block
#   block = 0, 阻塞主线程直到获得消息
#   block = k, 阻塞主线程最多k毫秒，若k毫秒内接收到数据返回结果，若k毫秒后无数据返回空值

streams = {stream: '$'}  # '$'是特殊ID，表示当前最大ID，意味着仅获取最新信息，忽略历史消息
pprint(r.xread(streams, block=1000))  # block=0会一直阻塞主线程直到获得数据

################################ stream信息 ################################

# 获取stream的详细信息，包括长度，最小ID, 最大ID等
pprint(r.xinfo_stream(stream))

# 获取消费组的信息
pprint(r.xinfo_groups(stream))

################################ 删除消息 ################################

# 由于数据会持久化在内存中，最好定时清除队列内的元素
print(r.xlen(stream))  # 当前消息的数量
print(r.xtrim(stream, maxlen=5))  # 删除太旧的消息，也可以用xdel(name, *ids)根据ID删除消息
