# coding = utf8

import time
import sys

"""
列表推导(list comprehension) vs 生成器表达式(generator expression)

列表推导会创建一个新的列表，当需要遍历的对象比较小时不存在任何问题，但
如果输入参数非常大，列表推导会占用大量内存，甚至引起程序崩溃，这时候应该
使用生成器表达式，它只在需要时进行计算，不会占用过多的内存。
"""

# 生成包含100万个数字的列表，计算所有偶数的和
def test_list_comprehension(arr):
    print("size of original array: %s" % sys.getsizeof(arr))  # bytes
    even_num = [x for x in arr if x % 2 == 0]  # 创建了新的列表
    print("size of new list: %s" % sys.getsizeof(even_num))
    res = sum(even_num)
    print("sum = %d" % res) 


def test_generator_expression(arr):
    # 用'()'代替'[]'即可创建生成器表达式
    # 它返回一个可迭代对象，只有在调用时才会进行运算
    # 可以使用内置的next方法逐次进行调用
    even_num = (x for x in arr if x % 2 == 0)
    print(type(even_num))
    #print(next(even_num))
    #print(next(even_num))
    res = sum(even_num)
    print("sum = %d" % res)


if __name__ == "__main__":

    arr = list(range(1000000))
    test_list_comprehension(arr)
    test_generator_expression(arr)



