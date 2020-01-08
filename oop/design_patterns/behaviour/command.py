"""
命令模式(Command Pattern)

如何理解命令模式？

将客户端请求与具体的执行严格区分，要求将请求封装成类。

如何实现命令模式？

命令模式涉及3个核心概念：
1. Receiver(接收者)：真正执行命令的类。
2. Command(命令)：代表客户端请求，通常包含Recevier对象，并提供公共接口execute,
    通过调用Recevier的方法实现功能。
3. Invoker(调用者)：负责处理命令，例如添加/删除/执行命令。

命令模式的优势是什么？

分而治之，同时满足客户端不同的需求。
"""

class Receiver:
    """接收者"""
    
    def action(self, desc):
        print(desc)


class Command:
    """抽象命令基类"""

    def __init__(self, receiver):
        self._receiver = receiver

    def execute(self):
        """提供执行命令的公共接口"""
        raise NotImplementedError()


class ConcreteCommandA(Command):
    """具体命令类"""

    def execute(self):
        self._receiver.action("Execute command A")


class ConcreteCommandB(Command):
    """具体命令类"""

    def execute(self):
        self._receiver.action("Execute command B")


class Invoker:
    """接收/删除/执行命令"""

    def __init__(self):
        self._commands = []

    def add_command(self, command):
        self._commands.append(command)

    def run(self):
        for command in self._commands:
            command.execute()


## 客户端负责创建具体命令和Invoker
receiver = Receiver()

command_a = ConcreteCommandA(receiver)
command_b = ConcreteCommandB(receiver)

invoker = Invoker()
invoker.add_command(command_a)
invoker.add_command(command_b)

invoker.run()

