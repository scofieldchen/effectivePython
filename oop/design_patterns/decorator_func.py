"""
装饰器函数：增强某函数的功能

考虑以下情景，如果要分析函数运行的时长，往往要记录开始运行的时间和结束运行的时间，
然后计算时间差并记录下来。整个逻辑与函数本身的逻辑没有关联，如果只是为了分析一个
函数，可以将代码写在函数内部，但如果要分析数十个函数，写在函数内部的方法使代码变得
非常冗余，这时候就应该把分析时间的代码抽象出来，卸载一个'装饰器函数'中。
"""

import time


def profiling_decorator(f):
    """装饰器函数，将被装饰的函数作为参数

    1. 在装饰器内部定义新函数，用于封装被装饰的函数，此处是加上分析运行时长的逻辑
    2. 使用*args, **kwargs传递参数
    3. 装饰器最终返回新函数作为结果，供外部调用
    """
    def wrapper(*args, **kwargs):
        start_time = time.time()
        res = f(*args, **kwargs)
        end_time = time.time()
        print("Computation time: %.2f seconds" % (end_time - start_time))
        return res

    return wrapper


#### 使用方法1：直接调用装饰器函数
# def func():
#     """被装饰的函数"""
#     print("doing complicated work...")
#     time.sleep(3)
#     return 0

# func = profiling_decorator(func)
# func()


#### 使用方法2：python装饰器

@profiling_decorator
def func():
    print("doing complicated work...")
    time.sleep(3)
    return 0

func()