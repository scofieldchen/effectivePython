"""
如何使用自定义logger？

1. 创建logger对象
2. 创建Handler(句柄)对象 ==> 如何处理日志信息
3. 创建Formatter对象 ==> 日志信息的格式
4. 将Formatter传递给Handler，将Handler传递给logger
5. 调用logger方法，如logger.info, logger.error等
"""

import time
import logging
from logging.handlers import TimedRotatingFileHandler


# 创建自定义logger对象
# __name__是调用logger的模块的名字，当项目存在多个python模块，这样设置非常方便
# 最好为logger设置全局level
# logger = logging.getLogger(__name__)
# logger.setLevel(logging.INFO)

# # 创建句柄(Handler)
# # Hanlder处理日志信息将输出到什么地方，如控制台，文件，邮件等
# handler_console = logging.StreamHandler()
# handler_file = logging.FileHandler("example.log")
# # 可以单独设置每一个handler的level
# handler_console.setLevel(logging.INFO)
# handler_file.setLevel(logging.WARNING)

# # 创建Formatter对象，并添加至Handler
# formatter_console = logging.Formatter("%(name)s - %(levelname)s - %(message)s")
# formatter_file = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
# handler_console.setFormatter(formatter_console)
# handler_file.setFormatter(formatter_file)

# # 将Handler传递给logger
# logger.addHandler(handler_console)
# logger.addHandler(handler_file)


def setup_logger(name, to_console=True, to_file=True, filename=None):
    """设置日志系统"""
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    format_str = "%(asctime)s-%(threadName)s-%(levelname)s-%(message)s"
    formatter = logging.Formatter(format_str)

    if to_console:
        handler_console = logging.StreamHandler()
        handler_console.setLevel(logging.INFO)
        handler_console.setFormatter(formatter)
        logger.addHandler(handler_console)

    if to_file and filename is not None:
        handler_file = TimedRotatingFileHandler(filename, when="midnight")
        handler_file.setLevel(logging.INFO)
        handler_file.setFormatter(formatter)
        logger.addHandler(handler_file)
    
    return logger


if __name__ == "__main__":
    logger = setup_logger(
        name="test",
        to_console=True,
        to_file=True,
        filename="test.log"
    )

    cnt = 0
    while cnt < 20:
        logger.info("test logging")
        cnt += 1
        time.sleep(1)