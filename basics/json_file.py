"""
什么是json?

json是存储和传输数据的方法。

json文件用键值对存储数据，支持数字，字符串，数组等数据结构。

python json库提供四个核心函数:

1. json.dump(data, io) -> 将数据写入json文件
2. json.load(io) -> 从json文件读取数据
3. json.dumps(data) -> 将python对象编码成json对象，存储在字符串中
4. json.loads(data) -> 将json对象解码成python对象
"""

import json
from pprint import pprint

# 要写入json文件的数据，支持字符串，数字，数组，甚至深层嵌套的数据结构
data = {
    "firstName": "Jane",
    "lastName": "Doe",
    "hobbies": ["running", "sky diving", "singing"],
    "age": 35,
    "children": [
        {
            "firstName": "Alice",
            "age": 6
        },
        {
            "firstName": "Bob",
            "age": 8
        }
    ]
}


# 将数据存储到本地json文件
with open("./tmp_data.json", "w") as json_file:
    json.dump(data, json_file)

# 读取本地json文件
with open("./tmp_data.json", "r") as json_file:
    data2 = json.load(json_file)
    pprint(data2)