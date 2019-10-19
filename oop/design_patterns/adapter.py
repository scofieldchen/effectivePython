"""
Adapter Pattern(适配器模式)

什么是适配器模式？

适配器模式用于调和两套不同系统的接口，接口不兼容的表现形式有很多，例如参数不同。
适配器模式仅使用一种情况，代码已经存在并难以更改，如果能直接更改代码，那么装饰器
模式更有效。

案例：
1. 一个国家产的电器插头可能与另一个国家产的插座不兼容，这时候需要转接口。
2. 一台笔记本电脑提供HDMI接口，但外接显示器提供VGA接口，这时候也需要转接口。

如何使用适配器模式？

模式涉及3个概念：客户端(client)，适配器(adapter)，适配者(adaptee)
client: 客户端是希望调用适配者接口的程序
adapter: 适配器负责调和不兼容的接口，它需要实例化适配者类，调用其接口，并返回
    客户端接口要求的内容
adaptee: 适配者是被适配的角色，它定义了客户端希望的的业务方法
"""


class Adapter:
    """适配器对象，实例化适配者并调用其接口"""

    def __init__(self):
        self._adaptee = Adaptee()

    def request(self):
        self._adaptee.specific_request()


class Adaptee:
    """适配者，实现了希望被客户端调用的接口"""

    def specific_request(self):
        pass


if __name__ == "__main__":

    adapter = Adapter()
    adapter.request()