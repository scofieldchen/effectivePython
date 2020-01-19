"""
在dict上进行运算: 求最小值，最大值和排序。
"""

# 假设记录股票价格的字典
prices = {
    "ETH/USDT": 158.25,
    "BTC/USDT": 8325.20,
    "XRP/USDT": 3.254,
    "EOS/USDT": 8.258
}

# 关键步骤：先用zip创建包含(values,keys)的可迭代对象，注意值放在第一位
# 然后调用min(), max(), sorted()函数，它们会根据元组的第一个元素计算

# 返回值最小的键值对
print(min(zip(prices.values(), prices.keys())))

# 返回值最大的键值对
print(max(zip(prices.values(), prices.keys())))

# 按值进行排序
print(sorted(zip(prices.values(), prices.keys())))  # 从小到大
print(sorted(zip(prices.values(), prices.keys()), reverse=True))  # 从大到小