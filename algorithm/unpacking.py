"""
序列解包(sequence unpacking): 将序列元素分解为多个变量。
"""

## 当序列元素较少
seq = [1, 2, 3]
x, y, z = seq
print(x, y, z)

## 序列元素较多，用'*'运算符，代表任意多元素
seq_2 = list(range(20))
seq_2

first, *middles, last = seq_2
print(first, last)
print(middles)

*items, last = seq_2
print(last)
print(items)