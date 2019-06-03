"""
创建一个自定义类，让它的行为类似于list,dict,set等原生数据结构，
但不知道要实现哪些方法，这时候可以使用collections库，它定义了很多抽象基类，
只要继承这些基类，就会强制你实现特定的方法。
"""

import collections


class Models(collections.Iterable):
    """继承Iterable令对象可以被遍历
    
    必须定义所有的特殊方法才能实例化对象，否则会报错，报错信息
    包含了要重写的特殊方法。

    除Iterable外，还可以继承Sequence(str or list),Mapping(dict)等。
    """
    
    def __init__(self):
        self.names = ["model1", "model2", "model3"]

    def __iter__(self):
        return iter(self.names)

models = Models()
for model in models:
    print(model)