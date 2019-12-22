"""
concurrent.futures提供了管理线程池的类ThreadPoolExecutor，
submit方法单独管理worker函数。
"""

import time
import random
from concurrent.futures import ThreadPoolExecutor, as_completed


# 定义worker函数
def cal_square(x):
    pause = random.randint(1,3)
    time.sleep(pause)
    return x ** 2

# 实例化ThreadPoolExecutor类，max_workers是线程数量
executor = ThreadPoolExecutor(max_workers=3)

# 用submit方法将worker函数‘提交’至线程池，返回Future对象
future_list = []
for i in range(3):
    future = executor.submit(cal_square, i)
    future_list.append(future)

# 调用Future对象的result方法
# result方法会阻碍线程直到获得结果或出现异常
for future in future_list:
    print(future.result())

# as_completed
# 当返回结果的顺序不重要时，可以使用as_completed函数，优先返回已经执行
# 完毕的worker函数的结果
future_list = [executor.submit(cal_square, i) for i in range(10)]
for f in as_completed(future_list):
    print(f.result())

# 使用上下文管理器(context manager)管理线程池
with ThreadPoolExecutor(max_workers=3) as executor:
    future_list = [executor.submit(cal_square, i) for i in range(10)]
    for f in as_completed(future_list):
        print(f.result())
