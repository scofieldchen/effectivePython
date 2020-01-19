"""
进程池(Process Pool): 多个工作进程的集合，方便管理。

通过multiprocessing.Pool对象实现进程池。

Pool对象提供几个核心方法：
1. map(): 将一个函数映射到多个输入，分几个进程并发执行，阻塞主进程直到返回结果，这是最常用的接口。
2. map_async(): map方法的变种，不阻塞主进程。
3. apply(): 将一个函数提交到进程池，阻塞主进程。
4. apply_async(): apply方法的变种，不阻塞主进程，返回结果对象，调用get方法获取结果。
"""

from multiprocessing import Pool


def worker(x):
    return x**2


def main():
    inputs = list(range(10))

    # processes定义工作进程的数量
    # Pool支持上下文管理器，__enter__返回进程池对象，__exit__调用terminate方法，停止工作进程
    with Pool(processes=4) as p:
        # map()将输入切割成很多部分，提交给进程池，并发执行任务
        # 阻塞主进程直到获得所有结果
        results = p.map(worker, inputs)
        print(results)

        # apply()将一个函数提交到进程池，阻塞直到返回结果
        res = p.apply(worker, args=(20,))
        print(res)  # should be 400

        # apply_async()将一个函数提交到进程池，不阻塞
        # 返回一个结果对象，调用get()方法获得结果
        res = p.apply_async(worker, args=(20,))
        print(res.get())


if __name__ == "__main__":
    main()
