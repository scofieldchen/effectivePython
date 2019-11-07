"""
上下文管理器(context-manager)

上下文管理器是实现了上下文管理协议(context-manager protocol)的对象，协议规定了
对象如何获取和释放资源。

如何在对象中实现上下文管理协议？

定义两个方法：

1. __enter__(self), 对象如何获取资源
2. __exit__(self, exc_type, exc_val, exc_tb)，对象如何释放资源

如何使用上下文管理器？

python用with ... as ...语法来调用上下文管理器。

何时使用上下文管理器？

当某个对象要获取和释放资源时就可以使用上下文协议，例如文件操作，数据库操作，网络通信等，
这些IO任务都需要先获得“连接”，操作数据，最后关闭连接。
"""

class MyDatabase:
    """创建一个模拟数据库操作的对象，实现
    上下文管理协议"""

    def __init__(self):
        pass

    def __enter__(self):
        """执行with A() as a时被调用，方法返回的值赋予a，
        定义如何获取资源，数据库操作首先要连接到数据库
        """
        print("connect to database")
        return self

    def __exit__(self, exc_type, exc_val, tb):
        """当with as中间的代码块运行完毕被调用，定义如何
        释放资源，在数据库操作中，最后要关闭数据库连接"""
        print("close connection")

    def insert(self):
        print("insert data into table")

    def delete(self):
        print("delete data from table")

    def update(self):
        print("update data in table")

    def query(self):
        print("query data from table")


# 用with as语法调用上下文管理器
with MyDatabase() as db:
    # db.__enter__()方法被调用
    db.insert()
    db.delete()
    db.update()
    db.query()
    # db.__exit__()方法被调用