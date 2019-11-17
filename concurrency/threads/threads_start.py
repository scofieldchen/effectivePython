"""
如何启动线程？
1. 创建Thread实例，提供target函数
2. start ==> 启动线程
3. join ==> 等待子线程结束并回归主线程
"""

import time
from threading import Thread


# 定义worker函数
def simple_worker(n):
    while n > 0:
        print("perform task %d" % n)
        n -= 1
        time.sleep(2)

# 启动线程
t = Thread(target=simple_worker, args=(10,))
t.start()

# 线程可以调用join方法，它会一直阻塞主线程直到子线程回归
# 如果线程需要长时间运行，例如用WS获取实时数据，可以将线程
# 设置为守护线程(后台线程)，将daemon设置为True，守护线程
# 不能调用join方法，在主线程结束时自动退出
t.join()

# 判断线程是否在运行？
if t.is_alive():
    print("thread running")
else:
    print("thread completed")