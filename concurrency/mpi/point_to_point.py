"""
点对点通信(Point to Point)

点代表进程，点对点通信即在进程间发送消息，一个进程是发送者，另一个是接收者。

允许传递的消息包括：1. python对象；2. numpy数组。
"""

from mpi4py import MPI


# 创建通信器对象，MPI程序为每条进程赋予一个被称为'等级(Rank)'的标识符
# 假设MPI程序创建k条进程，标识符将会是0, 1, 2, ... (k-1)
# comm对象有两个核心方法：send和recv
# comm.send: 向目标进程发送消息
# comm.recv: 接收消息
comm = MPI.COMM_WORLD

# 调用Get_rank()获取当前进程的标识符
rank = comm.Get_rank()

# 进程0发送消息
if rank == 0:
    data = {"a": 1, "b": "apple", "c": [1, 2]}
    comm.send(data, dest=1)  # dest是接收进程的标识符
    print(f"Process(0) send: {str(data)}")

# 进程1接收消息
if rank == 1:
    data = comm.recv(source=0)  # source是发送进程的标识符
    print(f"Process(1) recv: {str(data)}")
