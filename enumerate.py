# coding = utf8

"""
给定一个序列(sequence)，有3种遍历方法：
1. 根据元素进行遍历
2. 根据索引号遍历
3. 使用enumerate遍历，它能同时返回索引号和元素，效果最好
"""

symbols = ["EURUSD","GBPUSD","USDJPY","AUDUSD"]

# 直接遍历元素
for sym in symbols:
    print(sym)

# 根据索引进行遍历
for i in range(len(symbols)):
    print(symbols[i])

# 使用enumerate函数
for i,sym in enumerate(symbols):
    print("item %d: %s" % (i,sym))
