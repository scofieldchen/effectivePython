"""
观察者模式(observer pattern)

先创建一个核心对象，包含某些重要数据，然后创建一个或多个观察者对象，“观察”核心对象，
一旦数据发生变更，观察者对象可以把信息输出到控制台，日志文件，数据库或远程终端。

观察者模式通常用于备份系统。
"""

import time
import random


class Subject:
    """被‘观察’的核心对象，维护重要数据"""

    def __init__(self):
        self._observers = []
        self._data = 0

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data = value
        self._update_observers()  # 当核心数据发生变化，观察者对象开始工作

    def attach(self, observer):
        self._observers.append(observer)

    def remove(self, observer):
        try:
            self._observers.remove(observer)
        except ValueError:
            pass

    def _update_observers(self):
        for observer in self._observers:
            observer()
    
        
class ConsoleObserver:
    """观察者对象，当被观察对象的核心数据发生变化，
    输出信息至控制台"""

    def __init__(self, subject):
        self.subject = subject

    def __call__(self):
        print("subject.data ==> %d" % self.subject.data)


if __name__ == "__main__":

    subject = Subject()
    observer = ConsoleObserver(subject)
    subject.attach(observer)

    cnt = 0
    while cnt < 20:
        value = random.randint(0, 100)
        subject.data = value
        cnt += 1
        time.sleep(1)
    