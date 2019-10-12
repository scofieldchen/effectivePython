"""
builder pattern(建造者模式)

参考：
https://sourcemaking.com/design_patterns/builder
https://blog.csdn.net/shudaqi2010/article/details/53965917

什么是建造者模式?

考虑餐厅经营的情形，客户点了3份菜，随后点餐员将指令传达给不同的厨师，准备完毕后
把3份菜依次端给客户。这就是建造者模式的工作原理，涉及到两个概念：“建造者(builder)”和
“指挥者(director)”，建造者创建具体的产品(解决特定问题)，“指挥者”根据外部参数“指挥”建造者。
在上述案例中，点餐员充当“指挥者”的角色，厨师则是具体的“建造者”。

建造者模式和工厂模式的区别是什么？

工厂模式提供统一的接口创建“产品”，目的是返回对象实例，建造者模式直接使用“产品”，即调用
返回对象的方法。
"""

import abc


class VehicleBuilder(metaclass=abc.ABCMeta):
    """抽象的汽车建造者"""

    def __init__(self):
        self.doors = 0
        self.seats = 0
        self.horse_power = 0

    @abc.abstractmethod
    def build_engine(self):
        pass

    @abc.abstractmethod
    def build_doors(self):
        pass

    @abc.abstractmethod
    def build_seats(self):
        pass


class CarBuilder(VehicleBuilder):
    """具体的汽车建造者"""

    def build_engine(self):
        self.horse_power = 300

    def build_doors(self):
        self.doors = 4

    def build_seats(self):
        self.seats = 5


class BikeBuilder(VehicleBuilder):
    """具体的单车建造者"""

    def build_engine(self):
        self.horse_power = 50

    def build_doors(self):
        self.doors = 0

    def build_seats(self):
        self.seats = 1


class VehicleManufacturer(object):
    """制造汽车的‘指挥者(director)’"""

    def __init__(self):
        # 创建'builder'的方式很多，通常在类方法中实现
        self.builder = None

    def build(self):
        if self.builder is None:
            raise Exception("builder not found")
        self.builder.build_engine()
        self.builder.build_doors()
        self.builder.build_seats()

        print("vehicle detail:")
        print("horse power = %d" % self.builder.horse_power)
        print("doors = %d" % self.builder.doors)
        print("seats = %d" % self.builder.seats)
        

if __name__ == "__main__":

    manufacturer = VehicleManufacturer()

    manufacturer.builder = CarBuilder()
    manufacturer.build()

    manufacturer.builder = BikeBuilder()
    manufacturer.build()
