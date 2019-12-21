"""
装饰器模式(decorator pattern)

什么是装饰器模式？

“装饰”的定义是修改某个接口的行为，目的是实现定制化的需求。

装饰器模式涉及两个核心概念：装饰对象和核心对象。

核心对象：提供解决问题的接口，完成主要操作。
装饰对象：实例化核心对象，调用其接口，在调用前后进行修改，以达到增强其功能的目的。

装饰器模式和继承的区别？

两种方式都可以达到相同目的，但装饰器模式只会修改或增强某接口的功能，不
改变核心对象的代码，后者要求重写接口的所有代码，有时候会非常复杂。
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
