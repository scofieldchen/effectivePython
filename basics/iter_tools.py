"""
itertools

python标准库，提供一系列接口来操纵迭代器和可迭代对象。
"""

import itertools


## itertools.chain() --> 合并多个可迭代对象
lst = [1, 2, 3, 4]
tpl = (5, 6, 7, 8)
string = "kobe is the greatest basketball player"
print(list(itertools.chain(lst, tpl, string)))


## itertools.cycle --> 创建一个无限循环的迭代器
infinite_loop = itertools.cycle([1, 2, 3])
for _ in range(20):
    print(next(infinite_loop))


## itertools.zip_longest --> 两两匹配多个可迭代对象的元素
## 当可迭代对象的长度不一致，自动用None填充
lst_1 = [1, 2, 3]
lst_2 = ["a", "b", "c", "d", "e", "f"]
lst_3 = [4, 5, 6, 7]
print(list(itertools.zip_longest(lst_1, lst_2, lst_3)))
