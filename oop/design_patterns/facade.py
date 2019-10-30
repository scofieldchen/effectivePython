"""
门面模式(Facade Pattern)

什么是门面模式？

为复杂的系统创建简单和统一的接口，称为门面模式。

门面模式能解决什么问题？

1. 有多个复杂的子系统，解决问题时要同时使用多个，为提高效率，可以创建一个
“门面”类，将子系统全部封装起来，创建高度统一的接口供客户端使用。
2. 子系统的接口过于复杂以至于很难调用，这时可以创建一个新类，对子系统接口
进行封装，创建更简单的接口。

门面模式，装饰器模式，适配器模式的对比

三种模式都属于结构化模式，目标是处理不同对象之间的关系。装饰器模式“装饰”接口，
目的是增强功能，适配器主要解决新系统和旧系统接口不兼容的问题，门面模式则
把很多复杂的子系统封装起来，提供高度统一的接口。从实现方式来看，三种模式有相似
之处，但它们要解决的问题是不同的，区分设计模式的最佳方法不是从代码中找到差异，
而是从问题本身出发。
"""

class ComplexSubSystemA:
    """复杂子系统A"""

    def operation1(self):
        pass

    def operation2(self):
        pass


class ComplexSubSystemB:
    """复杂子系统B"""

    def operation3(self):
        pass

    def operation4(self):
        pass


class Facade:
    """门面类，封装子系统，提供更简单的统一接口"""

    def __init__(self):
        self._systemA = ComplexSubSystemA()
        self._systemB = ComplexSubSystemB()

    def operation(self):
        self._systemA.operation1()
        self._systemA.operation2()
        self._systemB.operation3()
        self._systemB.operation4()


facade = Facade()
facade.operation()  # 客户端仅需要调用统一接口，不需要理会底层细节