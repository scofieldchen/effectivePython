"""
Iterator Pattern(迭代器模式)

创建一个自定义类，可以用for循环迭代。

如何实现迭代器模式？

定义两个魔术方法：
1. __iter__: 被iter()函数调用时触发，返回迭代器本身
2. __next__: 被next()函数调用时触发，返回下一个元素，元素耗尽后主动引发'StopIteration'异常

只要理解python for循环的工作原理，就能明白为什么定义了上述两个魔术方法的对象能被迭代，
for loop首先会调用iter()函数创建一个迭代器, 然后在while循环中不断调用next()取出元素，
直到遇到StopIteration异常停止迭代。
"""

class MyList:

    def __init__(self, *args):
        self._data = args
        self.index = -1

    def __iter__(self):
        """返回实例本身"""
        return self

    def __next__(self):
        """返回下一个元素，元素耗尽时引发'StopIteration'异常"""
        self.index += 1
        if self.index >= len(self._data):
            raise StopIteration
        return self._data[self.index]


lst = MyList(1, 2, 3, 4, 5, 6)

# 用for loop迭代
for x in lst:
    print(x)