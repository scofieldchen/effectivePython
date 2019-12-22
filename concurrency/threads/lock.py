"""
线程同步机制：锁(Lock)

为什么需要锁？

当多条线程同时对公共资源进行修改时，可能导致'race condition(竞态条件)'，线程锁
能够避免这种情况发生，在同一个时刻，只允许一条线程修改公共资源。

如何理解锁？

锁可以理解为公共资源的'使用权'，锁有两种状态：“上锁”与“未上锁”。当线程A要修改公共
资源，先获取锁，这时锁的状态变为“上锁”，其它线程将无法获得锁，直到线程A释放锁，这时
锁的状态变为“未上锁”，其它线程可以获取锁，并修改资源。这样就避免了多条线程同时修改
资源导致意外的情况。

如何实现锁？

使用threading.Lock对象，提供两个核心方法：

1. acquire(): 上锁，锁的状态变为“上锁”，其它线程无法获得它。
2. release(): 解锁，锁的状态变为“未上锁”，其它线程可以获得它。

Lock对象支持上下文管理器。
"""

import threading


# 假设两个公共资源
shared_resource_1 = 0
shared_resource_2 = 0

lock = threading.Lock()


def increment_without_lock():
    global shared_resource_1
    for _ in range(1000000):
        shared_resource_1 += 1


def decrement_without_lock():
    global shared_resource_1
    for _ in range(1000000):
        shared_resource_1 -= 1


def increment_with_lock():
    global shared_resource_2
    for _ in range(1000000):
        lock.acquire()
        shared_resource_2 += 1
        lock.release()


def decrement_with_lock():
    global shared_resource_2
    for _ in range(1000000):
        lock.acquire()
        shared_resource_2 -= 1
        lock.release()


t1 = threading.Thread(target=increment_without_lock)
t2 = threading.Thread(target=decrement_without_lock)
t3 = threading.Thread(target=increment_with_lock)
t4 = threading.Thread(target=decrement_with_lock)

t1.start()
t2.start()
t3.start()
t4.start()

t1.join()
t2.join()
t3.join()
t4.join()

print(shared_resource_1)  # should not be 0
print(shared_resource_2)  # should be 0