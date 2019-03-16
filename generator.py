# coding = utf8

import time
import sys

# 列表推导(list comprehension) vs 生成器表达式(generator expression)
# 列表推导会创建一个新的列表，当需要遍历的对象比较小时不存在任何问题，但
# 如果输入参数非常大，列表推导会占用大量内存，甚至引起程序崩溃

# 案例：创建一个包含100万个数字的列表，计算所有数字的平方，最后求和
# 观察列表推导对内存的占用

def test_list_comprehension(arr):
    print("size of original array: %s" % sys.getsizeof(arr))
    even_num = [x**2 for x in arr]
    print("size of new list: %s" % sys.getsizeof(even_num))


if __name__ == "__main__":

    arr = list(range(1000000))
    test_list_comprehension(arr)



