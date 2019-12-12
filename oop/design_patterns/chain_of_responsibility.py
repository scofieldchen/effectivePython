"""
责任链模式(Chain of Responsibility)

如何理解责任链？

责任链：将一系列相似功能的类“串联”起来组成一条链，客户端请求沿着这条链一直传递，直到被处理。

责任链的工作原理与if else相似，不同之处在于将处理逻辑封装在类中，便于维护。

如何实现责任链？

1. 定义抽象基类，提供两个公共接口：指定继承者和处理请求。
2. 创建具体的请求处理类，继承抽象基类，实现不同的处理逻辑。
3. 创建责任链，指定每个请求类的继任者。
4. 启动责任链，将客户端请求在链中传递，处理请求。
"""

import abc


class Handler(metaclass=abc.ABCMeta):
    """抽象的请求处理类"""

    def __init__(self, successor=None):
        self._successor = successor  # 定义继承者，在链中传递请求

    @abc.abstractmethod
    def handle_request(self, request):
        """每个子类都必须提供处理接口"""
        pass


class ConcreteHandlerA(Handler):
    """具体的请求处理类"""

    def handle_request(self, request):
        if request >= 0 and request < 10:
            print("Handle request by HandlerA")
        elif self._successor is not None:
            self._successor.handle_request(request)


class ConcreteHandlerB(Handler):
    """具体的请求处理类"""

    def handle_request(self, request):
        if request >= 10 and request < 20:
            print("Handle request by HandlerB")
        elif self._successor is not None:
            self._successor.handle_request(request)


class DefaultHandler(Handler):
    """具体的请求处理类"""

    def handle_request(self, request):
        if request >= 20:
            print("Handle request by DefaultHandler")
        elif self._successor is not None:
            self._successor.handle_request(request)


# 假设客户端请求
request = [1, 2, 10, 99, 24, 15, 12, 18, 100]

# 创建责任链，设定每个请求类的继任者
default_handler = DefaultHandler()
handler_b = ConcreteHandlerB(default_handler)
handler_a = ConcreteHandlerA(handler_b)

# 处理请求
for x in request:
    handler_a.handle_request(x)