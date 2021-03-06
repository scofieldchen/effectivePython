"""
@property是装饰器，它可以将实例方法转化为对象属性，这是
在python class中使用setter和getter方法的有效途径.
"""

class Person:

    def __init__(self, name, age):
        self.name = name
        self._age = age  # _age是私有属性

    def __repr__(self):
        return "Person(name=%s, age=%s)" % (self.name, str(self.age))

    @property  # 将实例方法转换为属性
    def age(self):
        return self._age
    
    @age.setter  # 设置对象属性, 格式: @{property_name}.setter
    def age(self, value):  # setter方法与getter方法采用相同的名字，且接受value参数
        if value < 0:
            raise ValueError("age can't be less than 0")
        self._age = value


p = Person(name="alice", age=20)
print(p.name)
print(p.age)

p.age = 35
print(p.age)

p.age = -10  # raise ValueError
print(p.age)