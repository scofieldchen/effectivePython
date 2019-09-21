"""
装饰器模式(decorator pattern)

先创建一个核心对象，然后创建该对象的装饰器，“修饰”部分接口，提供新的功能，
接口名称保持一致。

装饰器与继承的区别在于：前者只会增加某接口的功能，不改变核心对象的代码，后者
会重新实现某接口，要求重写所有代码。
"""


class TextTag:
    """核心对象，代表html文本标签"""

    def __init__(self, text):
        self.text = text
    
    def render(self):
        return self.text


class BoldWrapper:
    """装饰核心对象，增强render功能"""

    def __init__(self, wrapper):
        self._wrapper = wrapper

    def render(self):
        return "<b>{}</b>".format(self._wrapper.render())


class ItalicWrapper:
    """装饰核心对象，增加render功能"""

    def __init__(self, wrapper):
        self._wrapper = wrapper

    def render(self):
        return "<i>{}</i>".format(self._wrapper.render())


if __name__ == "__main__":

    text = TextTag("hello world")
    print(text.render())
    print(BoldWrapper(text).render())
    print(ItalicWrapper(text).render())
    print(ItalicWrapper(BoldWrapper(text)).render())
