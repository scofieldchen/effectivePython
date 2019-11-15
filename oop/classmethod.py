"""
用classmethod实现新的构造器

类的构造方法默认使用__init__，有时候希望用多种方式创建实例，classmethod
能实现这一点，它接收一个默认参数'cls'，指向类本身。

classmethod会在底层调用__init__，创建新的实例。
"""

class Student:
    """代表学生的对象"""

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "Student(%s)" % self.name

    @classmethod
    def tom(cls):
        """cls参数指向类本身，在底层调用__init__创建实例"""
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
