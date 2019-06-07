"""
筛选序列的元素
"""

## 给定一个序列，同时包含正整数和负整数，筛选正整数

ints = [2, 1, -3, 4, -8, 9, -5, 6]

# 最简单的方法是列表推导
pos_ints = [x for x in ints if x > 0]
print(pos_ints)

# 除筛选外，列表推导还可以替换部分元素
ints2 = [x if x > 0 else 0 for x in ints]
print(ints2)


## 列表推导只适用简单情形，如果筛选条件很复杂，例如包含嵌套逻辑判断和异常处理，
## 最好适用filter加自定义函数

# 找出能转化为整数的元素
values = ['1', '2', '-3', '-', '4', 'N/A', '5']

def is_int(x):
    try:
        _ = int(x)
        return True
    except ValueError:
        return False

# filter将自定义函数(返回True或False)映射到序列的所有元素
# 保留结果为True的元素，最终返回迭代器
int_values = list(filter(is_int, values))
print(int_values)