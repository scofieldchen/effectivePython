"""
redis是内存型数据库，用键值对存储数据，能够实现读写高并发。

key是字符串，value的数据结构包含：

* string
* hash - 可理解为字典
* list
* set
* orderedSet
* stream - 消息队列
"""

import redis


######################### 建立连接 #########################

r = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

######################### 数据结构：字符串 #########################

# 增加/修改
r.set(name="user", value="kobe")  # 创建一个key:value对，若不存在则创建，若存在则更新value
r.mset({"user1": "bob", "user2": "james"})  # 创建多个key:value对
r.setex("foo", time=3, value="bar")  # 创建会过期的key:value对
r.append("user", "bryant")  # 在value后面追加内容

# 查询
print(r.get("user"))  # 获取一个键值对
print(r.mget(["user", "user1", "user2"]))  # 获取多个键值对

######################### 数据结构：hash #########################

# 增加/修改
# hset(name, key, value) --> name: {key:value}
# 数据结构类似于python的嵌套(一层)字典，{name: {key: value}}
r.hset(name="ethusdt", key="bid", value=36)  # 若key已存在不会更新value
r.hmset("ethusdt", mapping={"ask": 25.1, "time": 123456789})  # 在name对应的hash中批量设置键值对，若key不存在则创建新键值对，若key存在则更新value

# 查询
print(r.hget("ethusdt", "bid"))  # 根据name,key提取value
print(r.hmget("ethusdt", ["bid", "ask", "time"]))  # 获取name,keys对应的多个键值对的值
print(r.hgetall("ethusdt"))  # 获取name对应的所有键值对
print(r.hlen("ethusdt"))  # 获取name对应的键值对个数
print(r.hkeys("ethusdt"))  # 获取name对应的所有键
print(r.hvals("ethusdt"))  # 获取name对应的所有值
print(r.hexists("ethusdt", "bid"))  # 检查是否存在特定的键值对

# 删除
r.hdel("ethusdt", "bid")  # 删除name对应的某个键值对


######################### 数据结构：list #########################

# 增加/修改
r.lpush("list_name", 1)  # 创建一个键值对，值存储在列表中，若列表不存在则创建列表
r.lpush("list_name", 2, 3, 4)  # 同时往列表中插入多个值，从左侧添加，列表变为[4,3,2,1]
r.rpush("list_name", 5)  # 从右端添加元素，列表变为[4,3,2,1,5]
r.linsert("list_name", where="AFTER", refvalue="2", value="Bob")  # 在refvalue的前边(Before)或后边(After)插入value, 列表变为[4,3,2,Bob,1,5]
r.lset("list_name", index=0, value="Alice")  # 修改list[index]的value，列表变为[Alice,3,2,Bob,1,5]
r.lpop("list_name")  # 移除列表的第一个元素，列表变为[3,2,Bob,1,5]

# 查询
print(r.llen("list_name"))  # 返回name对应的列表的长度
print(r.lindex("list_name", index=0))  # 根据索引获取列表元素
print(r.lrange("list_name", start=0, end=-1))  # 根据切片获取列表元素，-1表示最后一个元素

# 删除
r.lrem("list_name", count=0, value="Bob")  # 删除count个等于value的元素，count=0表示删除全部
r.ltrim("list_name", start=0, end=2)  # 删除list[start:end]之外的所有元素
r.blpop(["list_name"])  # 逐个删除列表内的元素，按从左往右的顺序


######################### 常规命令 #########################

# r.delete("user")  # 删除name对应的键值对
# r.exists("user")  # 检测name对应的键值对是否存在
# r.expire("user", time=3)  # 为某个键值对设置超时时间
# r.rename(src="user", dst="user1")  # 修改name的名字
# r.move("user", db="db1")  # 将指定键值对移动到指定db

# redis-py每次执行请求都包含‘创建’和‘断开’连接操作
# 如果要在一次请求中执行多个命令，可以使用pipeline
pipe = r.pipeline(transaction=True)
r.set("user1", "alice")
r.set("user2", "apple")
r.set("user3", "king")
pipe.execute()