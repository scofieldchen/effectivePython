"""
Borg Pattern

Borg模式令同一个对象的不同实例共享状态。所谓共享状态，即所有实例共享属性，修改其中一个
实例的属性，其余所有实例的属性都会改变。

如何实现Borg模式？

python把类属性存储在'__dict__'，要实现Borg模式，先创建一个新的类属性'__share_state'，
然后在创建实例的时候将'__share_state'赋值给'__dict__'。

Borg模式解决哪些实际问题？

最经典的案例是数据库管理，参考以下案例：
https://github.com/onetwopunch/pythonDbTemplate/blob/master/database.py
"""

class Borg(object):
    
    __share_state = {}

    def __init__(self):
        self.__dict__ = self.__share_state
        self.state_1 = "123"
        self.state_2 = 658

    def __str__(self):
        return "state_1(%s) state_2(%s)" % (str(self.state_1), str(self.state_2))


if __name__ == "__main__":

    borg1 = Borg()
    borg2 = Borg()
    print(str(borg1))
    print(str(borg2))
    print(borg1 == borg2)  # borg1和borg2有共享的属性，但不是同一个实例

    borg1.state_1 = "scofield"
    borg1.state_2 = "alice"
    print(str(borg1))
    print(str(borg2))

    borg2.state_1 = 123
    borg2.state_2 = 562.025
    print(str(borg1))
    print(str(borg2))