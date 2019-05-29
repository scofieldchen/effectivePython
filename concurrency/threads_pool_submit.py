"""
concurrent.futures提供了管理线程池的类ThreadPoolExecutor，submit
方法单独管理worker函数。

submit返回Future对象，调用Future的方法来查询线程状态以及获得结果。

当有多个不同的worker函数时，应使用submit方法分开管理。
"""

import time
import random
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed


# worker函数
def cal_square(x):
    pause = random.random()
    print("%s: sleep %.2f seconds" % (threading.current_thread().name, pause))
    return x ** 2

# 实例化ThreadPoolExecutor类，max_workers是线程数量
executor = ThreadPoolExecutor(max_workers=3)

# 将worker函数'submit'至线程池，返回Future对象
future_list = []
for i in range(3):
    future = executor.submit(cal_square, i)
    future_list.append(future)

# 调用future的result方法得到计算结果
for future in future_list:
    print(future.result())  # result方法会阻碍直到返回结果或出现异常


## as_completed
# 当返回结果的顺序不重要时，可以使用as_completed函数，优先返回已经执行
# 完毕的worker函数的结果
future_list = [executor.submit(cal_square, i) for i in range(10)]
for f in as_completed(future_list):
    print(f.result())


## 使用上下文管理器(context manager)管理线程池
with ThreadPoolExecutor(max_workers=3) as executor:
    future_list = [executor.submit(cal_square, i) for i in range(10)]
    for f in as_completed(future_list):
        print(f.result())

