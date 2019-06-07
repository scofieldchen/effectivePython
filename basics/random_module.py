"""
用random模块实现随机抽样和生成随机数。
"""

import random


values = list(range(20))
print(values)

# 随机抽取1个元素
random.choice(values)

# 随机抽取n个元素，不放回抽样
random.sample(values, 3)

# 打乱元素的顺序
random.shuffle(values)
values

# 生成随机整数
random.randint(-100, 100)

# 生成均匀分布变量
random.uniform(1, 2)

# 生成正态分布变量
random.gauss(0, 1)
