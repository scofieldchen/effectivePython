# coding = utf8

"""
Python的内置函数zip允许同时遍历多个序列，每一轮迭代都会
返回一个元组，里边包含不同序列在相同的索引下对应的元素。
当迭代的序列的长度不同时，zip并不会报错而是“截断”多余的元素。
"""

# 同时迭代两个列表
names = ["bob", "alice", "david"]
ages = [20, 25, 35]
for name,age in zip(names,ages):
    print("name: %s, age: %d" % (name,age))

# 同时迭代两个以上的列表
genders = ["male", "female", "male"]
jobs = ["engineer", "teacher", "doctor"]
for name,age,gender,job in zip(names,ages,genders,jobs):
    print("name: %s, age: %d, gender: %s, job: %s" % (name,age,gender,job))

# 如果列表长度不一样
# 程序不会报错，但zip只会评估长度相同的那部分元素
names.append("kobe")  # 往names增加一个元素
for name,age in zip(names,ages):
    print(name,age)

# 如果不确定列表长度是否相同，或希望绕过zip的截断设定，
# 可以使用itertools模块的zip_longest函数
from itertools import zip_longest

for name,age in zip_longest(names,ages):
    print(name,age)