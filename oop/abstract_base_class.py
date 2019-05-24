"""
Abstract Base Class(ABC): 抽象基类

抽象基类的作用：
1. 强迫子类实现某些方法
2. 类型检查(type checking)
"""

from abc import ABCMeta, abstractmethod


## 定义抽象基类，强迫子类实现部分方法
# 假设我们要写自定义类模拟交通工具，如汽车，卡车，摩托车等，可以先定义
# 一个抽象基类(交通工具)，然后定义子类，子类中务必要实现start和stop方法

class Vehicle(metaclass=ABCMeta):
    """交通工具，子类应该实现start和stop"""

    @abstractmethod
    def start(self):
        pass
    
    @abstractmethod
    def stop(self):
        pass


class Car(Vehicle):

    def start(self):
        print("start the car")
    
    def stop(self):
        print("stop the car")


class Truck(Vehicle):

    def start(self):
        print("start the truck")
    
    def stop(self):
        print("stop the truck")


try:
    v = Vehicle()  # 抽象基类只提供接口，本身不可实例化
except Exception as e:
    print(e)

car = Car()
car.start()
car.stop()

truck = Truck()
truck.start()
truck.stop()


## 抽象基类的另一大用途是实现类型检查

if isinstance(car, Vehicle):
    print("car is Vehicle object")
else:
    raise TypeError("expect Vehicle object")
