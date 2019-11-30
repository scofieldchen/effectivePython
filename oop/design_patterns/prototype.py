"""
prototype pattern(原型模式)

原型模式是什么？

当我们要创建一个对象的大量实例，有两种方法：1. 创建所有的新实例，2. 先创建一个
实例，然后批量复制它，这种方法被称为“原型模式”。

为什么复制而不构造新实例？

类的实例化可能很复杂，例如包含打开文件和数据库以读取资料，甚至网络IO操作等，都会
耗费CPU和内存，如果同时创建上万个实例，将构成很大的性能压力，在这种情况下采用复制
或克隆的方式会更有效。

如何实现原型模式？

最高效的方法是使用copy模块的deepcopy函数，实现深层复制。

原型模式和工厂模式的区别是什么？

工厂模式创建不同的产品，原型模式克隆相同产品的“副本”。
"""

import copy


class Prototype:

    def __init__(self):
        # the construction might be very complicated
        # read database or file to get some data
        # fetch web api to get some information ...
        pass

    def clone(self):
        # 可以提供clone接口，也可以直接在外部调用deepcopy函数
        return copy.deepcopy(self)


def main():
    p = Prototype()  # 等待复制的原型
    p1 = copy.deepcopy(p)
    p2 = p.clone()
    
    print(p)
    print(p1)
    print(p2)
    
    
if __name__ == "__main__":
    main()