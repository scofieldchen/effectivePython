"""
Abstract Base Class(ABC): 抽象基类

抽象基类充当公共接口的“模板”，定义了子类要实现的属性和方法。

abc模块提供了创建自定义抽象基类的接口。

collections模块提供了很多可以使用的抽象基类，如'Container','Iterator'等。

抽象基类的作用：
1. 强迫子类实现方法和属性
2. 类型检查(type checking)
"""

from abc import ABCMeta, abstractmethod, abstractproperty


## 定义抽象基类，要求子类实现方法和属性
# 假设我们要写自定义类模拟交通工具，如汽车，卡车，摩托车等，可以先定义
# 一个抽象基类(交通工具)，然后定义子类，要求子类实现start和stop方法

class Vehicle(metaclass=ABCMeta):
    """交通工具，子类应该实现start和stop"""

    @abstractproperty
    def brand(self):
        pass

    @abstractmethod
    def start(self):
        pass
    
    @abstractmethod
    def stop(self):
        pass


class Car(Vehicle):
    brand = "BMW"

    def start(self):
        print("start the car")
    
    def stop(self):
        print("stop the car")


class Truck(Vehicle):
    brand = "GM"

    def start(self):
        print("start the truck")
    
    def stop(self):
        print("stop the truck")


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
