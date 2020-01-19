"""
如何用管道(Pipe)实现进程通信？

进程通过管道的两端交换数据，进程A从管道的一端发送消息，进程B从管道的另一端接收消息，反过来
进程B也可以向进程A发送消息。管道能够实现双向通信。

multiprocessing.Pipe

1. 调用Pipe()返回一对(conn1,conn2)连接对象，分别代表管道的两端，用于传送和接收数据。
2. Connection对象的核心方法：
    1.1 send() ==> 发送数据，必须是可序列化的对象
    1.2 recv() ==> 接收另一端发送的数据，阻塞进程直到获得元素，此外当另一端连接关闭且
        没有任何数据被接收，主动引发EOFError
    1.3 close() ==> 关闭连接

管道和队列的区别是什么？

队列实现单向通信，生产者负责生产，消费者负责消费；管道则实现双向通信，进程既可以充当生产者
也可以充当消费者。
"""

import logging
import random
import time
from multiprocessing import Pipe, Process

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(processName)s - %(message)s"
)


def worker1(conn1):
    """负责发送消息，类似于生产者"""
    for _ in range(10):
        item = random.randint(1, 100)
        conn1.send(item)
        logging.info(f"Send item {item}")
        time.sleep(1)
    
    conn1.send(None)


def worker2(conn2):
    """负责接收消息，类似于消费者"""
    while True:
        item = conn2.recv()  # 阻塞进程直到获得元素
        if item is None:
            break
        logging.info(f"Receive item {item}")


# Pipe()返回一对(conn,conn)连接对象，代表管道两端的连接
conn1, conn2 = Pipe(True)
# print(conn1, conn2)

proc1 = Process(target=worker1, args=(conn1,), name="worker1")
proc2 = Process(target=worker2, args=(conn2,), name="worker2")

proc1.start()
proc2.start()

proc1.join()
proc2.join()

