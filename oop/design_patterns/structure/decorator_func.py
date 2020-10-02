"""
装饰器函数：增强某函数的功能

考虑以下情景，如果要分析函数运行的时长，往往要记录开始运行的时间和结束运行的时间，
然后计算时间差并记录下来。整个逻辑与函数本身的逻辑没有关联，如果只是为了分析一个
函数，可以将代码写在函数内部，但如果要分析数十个函数，写在函数内部的方法使代码变得
非常冗余，这时候就应该把分析时间的代码抽象出来，放在一个'装饰器函数'中。
"""

import time
from memory_profiler import memory_usage

import numpy as np


def profiling_decorator(f):
    """评估函数运行时间和内存使用的装饰器函数

    1. 在装饰器内部定义新函数，用于封装被装饰的函数
    2. 使用*args, **kwargs传递参数
    3. 装饰器最终返回新函数作为结果，供外部调用
    """
    def wrapper(*args, **kwargs):
        t0 = time.time()
        res = f(*args, **kwargs)
        elapsed = time.time() - t0
        print(f"time: {elapsed:.3f} seconds")
        
        mem, res = memory_usage(
            (f, args, kwargs), retval=True, timeout=200, interval=1e-7)
        print(f"ram usage: {max(mem) - min(mem):.4f} mb")

        return res

    return wrapper


@profiling_decorator
def foo():
    arr = np.random.randn(10000, 3)
    return arr * 2

res = foo()
