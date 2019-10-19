"""
观察者模式(observer pattern)

创建一组观察者对象，“观察”核心对象的状态，当核心对象的某个属性发生变化时，
观察者对象会把信息打印到控制台，写入日志或数据库等。

观察者模式通常用于备份系统。
"""

import time
import random


class Subject:
    """被‘观察’的核心对象，维护重要数据"""

    def __init__(self):
        self._observers = []  # 观察者集合
        self._data = 0  # 核心数据

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
        self.subject = subject  # 将核心对象的实例作为参数

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
    