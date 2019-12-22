"""
继承threading.Thread类，创建线程子类，实现线程执行完毕后返回结果的功能。
"""

from threading import Thread


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

    t = ThreadWithReturnValue(target=worker, args=("this is result",))
    t.start()
    
    res = t.join()
    print(res)  # 应该打印'this is result'