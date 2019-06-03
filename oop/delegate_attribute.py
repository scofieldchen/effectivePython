"""
当一个类A作为另一个类B的属性，通常会从B中调用A的属性和方法，如果只需调用1-2个属性，
在B中重写即可，但如果要调用十几个方法，可使用__getattr__。
"""

class A:
    def __init__(self):
        self.x = 10

    def foo(self):
        print("call A.foo")

    def bar(self, x):
        print("call A.bar, x = %s" % str(x))


class B:
    """A的实例作为B的属性，从B中直接调用A的属性和方法"""
    def __init__(self):
        self.a = A()

    def __getattr__(self, name):
        """当调用B没有定义的属性时触发，令其返回A的属性"""
        return getattr(self.a, name)


b = B()
print(b.x)
b.foo()  # B.foo未定义，调用A.foo()
b.spam(10)  # B.spam未定义，调用A.spam(x)