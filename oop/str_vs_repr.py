"""
如何用字符串表示实例？

定义两个魔术方法：__str__和__repr__

1. print()和str()会调用__str__
2. repr()会调用__repr__，通常情况下__repr__应该返回实例的字符表示，这样
使用eval(repr(instance))就返回实例自身。python变成惯例。
3. 如果没有定义__str__，字符串函数会直接调用__repr__
"""

class Point:
    """笛卡尔坐标系的点"""

    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __str__(self):
        return "(%s, %s)" % (str(self.x), str(self.y))
    
    def __repr__(self):
        return "Point(%s, %s)" % (str(self.x), str(self.y))

p = Point(3, 4)

# 调用__str__，返回(3, 4)
print(p)
print(str(p))

# 调用__repr__，返回'Point(3, 4)'
print(repr(p))
print(type(eval(repr(p))))