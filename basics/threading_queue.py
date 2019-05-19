"""
用队列(queue)协同不同线程间的工作
"""

from threading import Thread
from queue import Queue

q = Queue()

def consumer():
    print("consumer waiting")
    q.get()  # 一直等待直到获得返回
    print("consumer done")

t = Thread(target=consumer)
t.start()

print("put something into queue")
q.put([1,2,3])

t.join()
print("terminate thread")