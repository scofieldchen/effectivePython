"""
工厂模式(Factory Pattern)

什么是工厂模式？

工厂模式是创建相似的对象的经典方法。考虑一种情况，在某个模块中有数十个相似的对象，它们
具有相同的接口，但处理不同的任务，如何能够根据所处理的问题选择合适的对象？最有效的方法
是创建一个”代理“的模块，我们提供参数给这个代理，让它帮助创建和返回需要的对象。这样做的
好处在于代码容易维护和拓展。

ccxt库就是实现工厂模式的现实案例，它包含了上百个交易所模块，提供相同的接口来获取数据和
管理订单。当客户端创建特定的交易所对象时，不会从ccxt直接引入类，而是通过统一的接口创建，
例如'client=ccxt.binance', 'client=ccxt.okex'。

https://realpython.com/factory-method-python/
https://python-3-patterns-idioms-test.readthedocs.io/en/latest/Factory.html


如何实现工厂模式？

工厂模式涉及3个概念：product, creator, client

1. product: 一个工厂包含很多'产品'，代表了解决问题的多种方式，它们既可以是自定义类，
    也可以是函数，在复杂系统中往往是提供相同接口的类。
2. creator: 根据参数返回'产品'，可以用类，函数或类方法实现。
3. client: 客户端程序，通过调用统一接口获得'产品'。客户端不直接与产品交互，而是调用
    creator的接口。

工厂模式能解决什么问题？

1. 替换复杂的逻辑判断(if-elif-else)
2. 根据外部数据源创建相似对象
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
    
    一般用自定义类实现'creator'，这里仅用函数实现
    """
    if type == "circle":
        return Circle
    if type == "square":
        return Square
    if type == "triangle":
        return Triangle
    
    raise Exception("invalid type")


class ShapeFactory(object):
    """抽象的形状工厂，提供统一接口，创建并返回实例"""
    
    def create_shape(self, type):
        return get_shape(type.lower())()


if __name__ == "__main__":

    shapes = ["circle", "square", "triangle"]
    factory = ShapeFactory()
    for shape in shapes:
        concrete_shape = factory.create_shape(shape)
        concrete_shape.draw()
        concrete_shape.erase()