"""
prototype pattern(原型模式)

什么是原型模式？

有时候我们要创建同一个类的大量实例，有两种方法，第一种方法是创建所有的新实例，第二种
方法是先创建一个“原型”，然后不断复制，仅仅修改部分属性。后者成为“原型”模式，
是批量创造实例的有效模式。

为什么使用原型模式？

从性能上考虑，复制对象比创建对象高效。

原型模式和工厂模式的区别是什么？

工厂模式有很多不同产品，原型模式复制了很多同一个产品的“副本”。
"""

import copy


class Prototype:
    """原型对象"""    
    pass


def main():
    p = Prototype()  # 等待复制的原型
    p1 = copy.deepcopy(p)
    p2 = copy.deepcopy(p)
    
    print(p)
    print(p1)
    print(p2)
    
    
if __name__ == "__main__":
    main()