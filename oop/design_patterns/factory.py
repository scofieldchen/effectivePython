"""
工厂模式(Factory Pattern)

原理：提供创建相似对象的接口。考虑ccxt，当我们想创建特定的交易所对象时，不会从ccxt的
子模块中引入类，而是通过ccxt提供的统一接口进行创建，例如'client=ccxt.binance'或者
或者'client=ccxt.okex'，返回的对象又提供相同的方法。这种设计模式隐藏了具体对象，
客户端程序通过调用统一的接口来实现想要的内容，好处在于代码容易维护和拓展。

https://realpython.com/factory-method-python/
https://python-3-patterns-idioms-test.readthedocs.io/en/latest/Factory.html

工厂模式涉及3个概念：product, creator, client
1. product: 一个工厂包含很多'产品'，代表了解决问题的多种方式，具体的实现可以是
    创建自定义对象，函数或类方法。
2. creator: 根据参数返回具体'产品'，具体实现可以是自定义类，函数或类方法，在简单
    工厂模式下，一个函数或类方法已经满足需求。
3. client: 客户端程序，通过调用统一的接口返回具体的'产品'。

使用场景：
1. 替换复杂的逻辑判断(if-elif-else)
2. 根据外部数据源创建相似的对象
3. 用多种不同方法实现某一个目的(类似策略模式)
4. 整合类似的外部服务
"""

class Shape(object):
    """抽象形状类"""
    pass


class Circle(Shape):
    """具体形状类：圆"""

    def draw(self):
        print("Draw a circle")

    def erase(self):
        print("Erase a circle")


class Square(Shape):
    """具体形状类：正方形"""

    def draw(self):
        print("Draw a square")

    def erase(self):
        print("Erase a square")


class Triangle(Shape):
    """具体形状类：三角形"""

    def draw(self):
        print("Draw a triangle")

    def erase(self):
        print("Erase a triangle")


def get_shape(type):
    """根据参数选择具体对象
    
    一般用自定义类实现'creator'，此处仅用函数作为说明
    """
    if type == "circle":
        return Circle
    elif type == "square":
        return Square
    elif type == "triangle":
        return Triangle
    else:
        raise Exception("invalid type")


class ShapeFactory(object):
    """抽象的形状工厂
    
    提供统一接口，创建具体的对象
    """
    
    def create_shape(self, type):
        return get_shape(type.lower())()


if __name__ == "__main__":

    shapes = ["circle", "square", "triangle"]
    factory = ShapeFactory()
    for shape in shapes:
        concrete_shape = factory.create_shape(shape)
        concrete_shape.draw()
        concrete_shape.erase()

