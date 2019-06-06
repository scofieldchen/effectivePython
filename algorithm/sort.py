"""
使用sorted函数进行排序
"""

## 对序列进行排序

# 假设两个列表，分别存储名字和对应的年龄
# 字符串和数字是最常见的待排序数据
names = ["kobe", "tracy", "bob", "alice", "louis"]
ages = [20, 25, 18, 56, 32]

print(sorted(names))  # 对字符串排序
print(sorted(ages))  # 对数字排序，从小到大
print(sorted(ages, reverse=True))  # 从大到小


## 对字典进行排序
# sorted()有一个参数key，接受可调用函数，该函数会赋予所有元素一个“标签”，
# 然后按照这个“标签”对元素进行排序

names_ages = {}
for name,age in zip(names, ages):
    names_ages[name] = age
print(names_ages)

# 按value进行排序
print(sorted(names_ages.items(), key=lambda x: x[1]))

# 按key进行排序
print(sorted(names_ages.items(), key=lambda x: x[0]))


## 对自定义类进行排序

class Item:
    
    def __init__(self, id):
        self.id = id

    def __repr__(self):
        return "Item(%d)" % self.id
    
items = [Item(1002), Item(1005), Item(32), Item(65)]
print(items)

# 按照产品id进行排序
print(sorted(items, key=lambda x: x.id))