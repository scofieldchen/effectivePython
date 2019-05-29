"""
concurrent.futures提供了管理线程池的类ThreadPoolExecutor，
map方法将同一个worker函数映射到不同的参数，在多条线程执行运算，
如果worker函数返回结果，map将按输入参数的顺序返回结果。
"""

import time
import random
import threading
from concurrent.futures import ThreadPoolExecutor


# 定义简单的worker函数，接受一个参数
def cal_square(x):
    pause = random.random()
    print("%s: sleep %.2f seconds" % (threading.current_thread().name, pause))
    return x ** 2


executor = ThreadPoolExecutor(max_workers=4)
inputs = [1, 2, 3, 4]
results = executor.map(cal_square, inputs)  # 返回迭代器
print(list(results))  # 按输入参数的顺序返回结果


# worker函数接受多于两个的参数
def cal_sum(x, y, z):
    return x + y + z

x = [1, 2, 3]
y = [4, 5, 6]
z = [7, 8, 9]

# 按顺序传递迭代对象，map自动调用zip将参数进行配对
results2 = executor.map(cal_sum, x, y, z)
print(list(results2))
