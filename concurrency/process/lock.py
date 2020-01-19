"""
如何实现进程同步？

同步原理与线程相似，为了避免多进程同时修改共享资源导致冲突，从multiprocessing库引入
Lock, Event, Condition等对象。

线程和进程的区别？

线程存在于进程内部，它们共享内存空间，但进程拥有自己的内存空间，所以进程同步不是一个
很重要的问题。
"""

import multiprocessing
from multiprocessing import Process, Lock


# 创建共享变量(相同的内存空间)
# 不同进程有自己的内存空间，必须使用以下方式才能在进程间创建共享变量
shared_resource_1 = multiprocessing.Value("i", 1)  # 第一个参数'i'表示'integer'
shared_resource_2 = multiprocessing.Value("i", 1)

lock = Lock()


def increment_without_lock(shared_resource):
    for _ in range(100000):
        shared_resource.value += 1


def decrement_without_lock(shared_resource):
    for _ in range(100000):
        shared_resource.value -= 1


def increment_with_lock(shared_resource, lock):
    for _ in range(100000):
        lock.acquire()
        shared_resource.value += 1
        lock.release()


def decrement_with_lock(shared_resource, lock):
    for _ in range(100000):
        lock.acquire()
        shared_resource.value -= 1
        lock.release()


p1 = Process(target=increment_without_lock, args=(shared_resource_1,))
p2 = Process(target=decrement_without_lock, args=(shared_resource_1,))
p3 = Process(target=increment_with_lock, args=(shared_resource_2, lock))
p4 = Process(target=decrement_with_lock, args=(shared_resource_2, lock))

p1.start()
p2.start()
p3.start()
p4.start()

p1.join()
p2.join()
p3.join()
p4.join()

print("without lock: ", shared_resource_1.value)  # should not be 1
print("with lock: ", shared_resource_2.value)  # should be 1