"""
建造者模式(Builder Pattern)

https://sourcemaking.com/design_patterns/builder
https://mozillazg.com/2016/08/python-builder-pattern.html

如何理解建造者模式？

建造者模式的核心思想是将创建复杂对象的过程与对象的具体表现相分离。

以创建网页表单为例，网页表单有很多种表现形式，包含不同类型的字段和样式。首先创建builder对象，
提供公共接口来设置字段，然后创建director对象，接收外部参数逐步构建表单，构建过程要调用builder
提供的接口，最终返回表单对象的实例。

如何实现建造者模式？

通用实现模式要创建3个对象：

1. product: 具体的产品
2. builder: 建造者，提供共同接口来创建产品，将product作为属性
3. director: 指挥者，根据外部参数来构建产品，实例化builder对象作为属性，调用
    builder提供的接口来创建具体的产品

建造者模式和工厂模式有什么区别？

两种模式的共同点是提供了创建产品的统一接口，不同点是工厂模式“一次性”的返回对象，
但建造者模式必须根据外部参数逐步构建，最终返回复杂的对象。
"""

import abc


class Vehicle(object):
    """具体产品"""

    def __init__(self):
        self.doors = 0
        self.seats = 0
        self.horse_power = 0

    def display(self):
        print("horse power = %d" % self.horse_power)
        print("doors = %d" % self.doors)
        print("seats = %d" % self.seats)


class VehicleBuilder(metaclass=abc.ABCMeta):
    """抽象的建造者"""

    def __init__(self):
        self.vehicle = Vehicle()

    @abc.abstractmethod
    def build_engine(self):
        return

    @abc.abstractmethod
    def build_doors(self):
        return

    @abc.abstractmethod
    def build_seats(self):
        return


class CarBuilder(VehicleBuilder):
    """具体的汽车建造者"""

    def build_engine(self):
        self.vehicle.horse_power = 300

    def build_doors(self):
        self.vehicle.doors = 4

    def build_seats(self):
        self.vehicle.seats = 5


class BikeBuilder(VehicleBuilder):
    """具体的单车建造者"""

    def build_engine(self):
        self.vehicle.horse_power = 50

    def build_doors(self):
        self.vehicle.doors = 0

    def build_seats(self):
        self.vehicle.seats = 1


class VehicleManufacturer(object):
    """制造汽车的指挥者(director)"""

    def __init__(self):
        self.builder = None

    def build(self):
        if self.builder is None:
            raise Exception("builder not found")
        self.builder.build_engine()
        self.builder.build_doors()
        self.builder.build_seats()

        return self.builder.vehicle
        

if __name__ == "__main__":

    # 创建指挥者
    manufacturer = VehicleManufacturer()

    # 为指挥者设定具体的builder，开始构建
    manufacturer.builder = CarBuilder()
    car = manufacturer.build()
    car.display()

    manufacturer.builder = BikeBuilder()
    bike = manufacturer.build()
    bike.display()
