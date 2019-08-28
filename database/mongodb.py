"""
mongoDB使用教程

安装和配置(linux)
https://docs.mongodb.com/v3.4/tutorial/install-mongodb-on-ubuntu/

pymongo教程
https://api.mongodb.com/python/current/tutorial.html

mongo shell教程
https://docs.mongodb.com/manual/mongo/
"""

from pprint import pprint
import pymongo
from pymongo import MongoClient


## 连接mongoDB
# --------------------------------------------------------------------
client = MongoClient("localhost", 27017)


## 接入数据库
# --------------------------------------------------------------------

# mongoDB包含很多子数据库，后者理解为前者的属性，用‘.’方法访问
# 如果数据库不存在，插入数据后会自动创建
# 创建/接入一个名为'pymongo_test'的数据库
db = client.pymongo_test

# 查询有哪些数据库，只有在插入数据后才会真正创建
# client.list_databases()
# client.list_database_names()


## 插入数据
# --------------------------------------------------------------------

# mongoDB有两个核心概念，Collection和Document，类似于关系型数据库的表格(table)和行(row)
# 从属关系和访问方法：mongoDB.Database.Collection.Document
# Collection是一系列Document的集合
# mongoDB使用JSON存储数据，pymongo则使用字典表示Document

# 创建/获取一个名为'users'的Collection
users = db.users

# 查询当前数据库有哪些collections，只有在插入数据后才会真正创建
# db.list_collections()
# db.list_collection_names()

# 插入一条数据(document)
user = {
    "name": "kobe",
    "age": 25,
    "job": "teacher"
}
res = users.insert_one(user)
print(res.inserted_id)

# 插入多条数据
user1 = {
    "name": "iris",
    "age": 32,
    "job": "worker"
}
user2 = {
    "name": "bob",
    "age": 45,
    "job": "banker"
}
user3 = {
    "user": "kyle",
    "age": 18,
    "job": "student"
}
res = users.insert_many([user1, user2, user3])
print(res.inserted_ids)


## 获取数据
# --------------------------------------------------------------------

# 使用find_one获取一条数据，默认返回第一条
res = users.find_one()
pprint(res)

# 根据筛选条件返回一条数据
res = users.find_one({"name": "kobe"})
pprint(res)

# 如果找不到记录，不会报错，直接返回None
res = users.find_one({"name": "scofield"})
print(res)

# 使用find获取多条数据，find方法返回cursor对象，表示返回结果的数量，可迭代
results = users.find()
for res in results:
    pprint(res)

# 将筛选条件传入find，返回符合条件的结果
results = users.find({"name": "kobe"})
for res in results:
    pprint(res)

# count_documents：统计当前Collection包含多少条记录
print(users.count_documents({}))

# 统计满足筛选条件的数据的数量
print(users.count_documents({"name": "kobe"}))

# 范围查询, 高级查询方法和运算符查询官方文档
results = users.find({"age": {"$gt": 30}})
for res in results:
    pprint(res)
