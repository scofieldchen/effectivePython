"""
@staticmethod: 装饰器

静态方法类似于函数，不同之处在于它的命名空间是class本身，静态方法无法修改
类和实例的状态，因为它不接受self或者cls参数。

使用静态方法的场景：分离部分计算逻辑，明确告诉开发者不能修改对象状态。
"""

import math


class Circle:

    def __init__(self, radius):
        self.radius = radius  # 半径

    def area(self):
        # 调用实例方法计算面积
        return math.pi * self.radius ** 2

    @staticmethod
    def cal_area(radius):
        # 调用静态方法计算面积
        return math.pi * radius ** 2


circle = Circle(radius = 3)

print(circle.area())
print(circle.cal_area(radius=3))
