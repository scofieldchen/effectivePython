"""
模板模式(Template Pattern)

什么是模板模式？

将重复部分代码抽离出来，放在“模板”模块中，称为模板模式，模板模式
是经典的“DRY(Don't Repeat Yourself)”原则的最佳表现。

模板模式的应用场景有哪些？

假设有很多相似的类，大部分方法都处理相同的问题，例如连接数据库，读取/写入文件等，
只有部分核心方法的逻辑不同，这时就可以使用模板模式，具体实现：创建一个抽象基类，
实现具有相同功能的方法，让子类重写部分核心方法。
"""

class Template:
    """抽象基类，作为子类的模板"""

    def prepare_data(self):
        """模板方法，直接供子类调用"""
        print("implemented by base class")

    def process_data(self):
        """要求子类重写"""
        raise NotImplementedError  # 常用方式

    def serialize_data(self):
        """模板方法，直接供子类调用"""
        print("implemented by base class")


class ConcreteImplementA(Template):
    """继承模板，只需重写核心方法"""

    def process_data(self):
        print("do something")

    def run(self):
        self.prepare_data()
        self.process_data()
        self.serialize_data()


class ConcreteImplementB(Template):
    """继承模板，只需重写核心方法"""

    def process_data(self):
        print("do something")

    def run(self):
        self.prepare_data()
        self.process_data()
        self.serialize_data()

