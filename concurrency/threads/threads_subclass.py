"""
如果要创建Thread对象的子类，必须重写run()方法，才能调用worker函数。
"""

from threading import Thread
import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(threadName)s - %(message)s"
)


class MyThread(Thread):
    """最简单的继承"""
    def run(self):
        logging.info("running")


class ThreadWithReturnValue(Thread):
    """Thread对象默认不返回内容，重写run和join方法令其返回计算结果"""
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, daemon=None):
        super().__init__(group=group, target=target, name=name,
                         args=args, kwargs=kwargs, daemon=daemon)
        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)
    
    def join(self, *args):
        Thread.join(self, *args)
        return(self._return)


def worker(x):
    return(x)


if __name__ == "__main__":

    #t = MyThread()
    #t.start()

    t = ThreadWithReturnValue(name="myThread", target=worker, args=("king",))
    t.start()
    res = t.join()
    logging.info(res)