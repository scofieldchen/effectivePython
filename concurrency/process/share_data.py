"""
如何在不同进程共享数据？

进程有自己的内存空间，当父进程生成子进程时，子进程复制了父进程的所有变量，当子进程试图修改
这些变量时，父进程的变量保持不变。

在线程编程中，防止竞态条件是关键问题(线程同步)，而在进程编程中，实现共享数据是关键问题。

一般情况下，并发编程避免使用共享数据，但当必须这么做时，multiprocessing提供了两种方式：
1. 共享内存；2. 服务进程。
"""

## 子进程无法直接修改父进程的数据
# from multiprocessing import Process

# x = 1  # 创建全局变量，整数
# l = []  # 全局变量，列表

# def worker(x, l):
#     """在子进程中试图修改父进程创建的变量"""
#     x = 2  # 改变整数的值
    
#     # 为列表添加新的元素
#     for i in range(10):
#         l.append(i)

# p = Process(target=worker, args=(x, l))

# p.start()
# p.join()

# print(x)  # x仍然为1
# print(l)  # l仍然为空列表


## 共享内存
# 创建共享内存的数据结构，不同的进程都可以修改
# from multiprocessing import Process, Value, Array
# import random

# share_x = Value("d", 1.0)  # 共享内存的双精度浮点值'1.0'
# share_arr = Array("i", range(10))  # 共享内存的整型数组'[0,1,2...9]'
# print("original x: ", share_x.value)
# print("original array: ", share_arr[:])

# def worker(share_x, share_arr):
#     share_x.value = 2.0  # 将数值从1.0变为2.0

#     # 任意填充数组的元素
#     for i in range(len(share_arr)):
#         share_arr[i] = random.randint(1, 100)

# p = Process(target=worker, args=(share_x, share_arr))
# p.start()
# p.join()

# print("modified x: ", share_x.value)
# print("modified array: ", share_arr[:])


## 服务进程
# multiprocessing提供Manager对象，该对象管理一个服务进程，该进程保留任意类型的全局
# 变量，允许其它进程修改变量。这种方式比共享内存更加灵活。

from multiprocessing import Process, Manager

manager = Manager()
share_vars = manager.Namespace()  # 以对象属性的方式存储共享内存的变量
share_vars.x = 1.0
share_vars.y = 2
share_list = manager.list()

print("shared variables: ", str(share_vars))
print("shared list: ", str(share_list))

def worker(share_vars, share_list):
    share_vars.x = 2.0
    share_vars.y = 1

    for i in range(10):
        share_list.append(i)
    
p = Process(target=worker, args=(share_vars, share_list))
p.start()
p.join()

print("modified shared variables: ", str(share_vars))
print("modified shared list: ", str(share_list))
