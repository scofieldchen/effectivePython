"""
@classmethod: 装饰器

类方法接受默认参数cls，指向class本身。

classmethod的一个用途是充当构造器，可以在类方法
内部构造并返回该对象的实例。
"""

class Student:
    """代表现实的学生对象"""

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "Student(%s)" % self.name

    @classmethod
    def tom(cls):  # classmethod的第一个参数默认写cls，指向Student Class
        return cls(name="Tom")
    
    @classmethod
    def alice(cls):
        return cls(name="Alice")

    @classmethod
    def a_few_students(cls, names):
        return [cls(name) for name in names]

# 用标准方法创建Student类的实例
student = Student("Tom")
print(student)

# 用classmethod构建Student的实例
student2 = Student.tom()
print(student2)

# 生成多个Student对象的实例
names = ["tom", "alice", "kobe", "bob"]
students = Student.a_few_students(names)
for stu in students:
    print(stu)
