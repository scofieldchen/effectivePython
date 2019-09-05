"""
pickle: 序列化python对象

pickling: 将python对象转化为二进制文件，存储在本地
unpickling: 将二进制文件转化为python对象
"""

import pickle


## pickling(序列化)python数据结构
example_dict = {"name": "kobe", "age": 25, "job": "banker"}

with open("./database/test.pickle", "wb") as outfile:
    pickle.dump(example_dict, outfile)

## unpickling
with open("./database/test.pickle", "rb") as infile:
    res = pickle.load(infile)

print(res)


## pickling custom class

