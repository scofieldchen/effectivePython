"""
线程对象没有主动停止的方法，如果想关闭子线程，必须创建自定义类，
设置好停止线程的开关，在合适的时机终止线程。
"""

import time
from threading import Thread


class MyTask:

    def __init__(self):
        # 设置是否终止线程的开关
        self._running = True

    def terminate(self):
        self._running = False

    def run(self, n):
        # 在子线程中调用run方法
        # 将self._running设置为False，作为终止线程的信号
        while self._running and n > 0:
            print("perform task %d" % n)
            n -= 1
            time.sleep(2)


task = MyTask()
t = Thread(target=task.run, args=(30,))
t.start()

time.sleep(5)
task.terminate()  # 终止线程
t.join()

if t.is_alive():
    print("thread running")
else:
    print("thread stop")
