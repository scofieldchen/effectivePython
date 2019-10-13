"""
builder pattern(建造者模式)

https://sourcemaking.com/design_patterns/builder
https://blog.csdn.net/shudaqi2010/article/details/53965917

什么是建造者模式?

将创建复杂对象的过程和具体实现相分离。考虑造车的情形，车辆是非常复杂的产品，包含发动机，底盘，
风向盘和座椅等元素，不同车型的配件又完全不同，为了有效的生产，需要将造车的过程分而治之，使用
不同的车间造对应的零件，有一个“指挥”中心负责安排生产。

建造者模式设计两个概念：“建造者(builder)”和“指挥者(director)”，前者负责创建具体的产品，后者
根据外部参数“指挥”建造者。最终目标是返回一个复杂的对象。

建造者模式和工厂模式的区别是什么？

两种模式的共同点是提供了统一的接口，不同之处在于，工厂模式“一次性”的返回对象，但建造者模式
必须逐步构建对象，最终返回产品。
"""

import abc


class Vehicle(object):
    """汽车：复杂的产品"""

    def __init__(self):
        self.doors = 0
        self.seats = 0
        self.horse_power = 0

    def display(self):
        print("horse power = %d" % self.horse_power)
        print("doors = %d" % self.doors)
        print("seats = %d" % self.seats)


class VehicleBuilder(metaclass=abc.ABCMeta):
    """抽象的汽车建造者"""

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
        # 逐步构建“汽车”这个复杂的产品，最终返回对象实例
        if self.builder is None:
            raise Exception("builder not found")
        self.builder.build_engine()
        self.builder.build_doors()
        self.builder.build_seats()

        return self.builder.vehicle
        

if __name__ == "__main__":

    manufacturer = VehicleManufacturer()

    manufacturer.builder = CarBuilder()
    car = manufacturer.build()
    car.display()

    manufacturer.builder = BikeBuilder()
    bike = manufacturer.build()
    bike.display()
