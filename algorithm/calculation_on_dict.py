"""
在dict上进行运算，如求最小值，最大值和排序。
"""

# 假设记录货币成交量的字典
volumes = {
    "ETH/USDT": 1000,
    "BTC/USDT": 1200,
    "XRP/USDT": 500,
    "EOS/USDT": 400
}

# 如何返回成交量最小的(key, value)对？

# 常用方法是分别计算最小成交量和对应的货币对，然后组合在一起输出
min_vol = min(volumes.values())
symbol = min(volumes, key=lambda k: volumes[k])
print((symbol, min_vol))

# 更有效的方法是利用zip构建(value, key)的迭代对象，再传递给min
min(zip(volumes.values(), volumes.keys()))

# 同理快速找出成交量最大的(key, value)对
max(zip(volumes.values(), volumes.keys()))

# 按成交量排序
sorted(zip(volumes.values(), volumes.keys()))

# 也可以指定sorted的key参数，按照成交量进行排序
sorted(volumes.items(), key=lambda x: x[1])
