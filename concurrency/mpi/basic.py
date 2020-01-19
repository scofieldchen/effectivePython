"""
mpi4py编程初步

multiprocessing和mpi4py提供了两种不同的多进程编程范式。

multiprocessing要求创建Process类，定义target函数等，mpi4py则不要求这么做，后者
由外部程序创建并管理进程，类似于进程池，mpi4py提供了强大的进程通信机制，包括点对
点通信和聚合通信。
"""

from mpi4py import MPI


# 创建通信器对象
comm = MPI.COMM_WORLD

# 每条进程被赋予一个称为等级(rank)的非负整数
rank = comm.Get_rank()

print(f"Process({rank}) is running")

# 终端执行命令运行脚本：mpiexec -n k python your_script.py
# k是进程数量，your_script.py是要运行的脚本
