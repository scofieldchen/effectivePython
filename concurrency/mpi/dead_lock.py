"""
死锁问题(DeadLock Problem): 两个进程相互阻塞，进程A等待进程B完成某些任务，进程B
等待进程A完成某些任务，结果两个进程都无法进行。
"""

import logging
from mpi4py import MPI

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# 创建通信器对象
comm = MPI.COMM_WORLD

# 获取当前进程的标识符
rank = comm.Get_rank()

# 假设两条进程，进程0先从进程1接收消息，然后向进程1发送消息；进程1先从进程0接收消息，然后向进程0发送消息
# 导致两条进程相互阻塞，即死锁问题

if rank == 0:
    logging.info("Process(0): recv data from Process(1)")
    data_recv = comm.recv(source=1)
    logging.info("Process(0): %s" % str(data_recv))
    
    logging.info("Process(0): send data to Process(1)")
    data_send = {"a": 1, "b": 2}
    comm.send(data_send, dest=1)

if rank == 1:
    logging.info("Process(1): recv data from Process(0)")
    data_recv = comm.recv(source=0)
    logging.info("Process(1): %s" % str(data_recv))
    
    logging.info("Process(1): send data to Process(0)")
    data_send = {"c": 3, "d": 4}
    comm.send(data_send, dest=0)