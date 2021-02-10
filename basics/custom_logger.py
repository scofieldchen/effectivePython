"""
如何使用自定义logger？

1. 创建logger对象
2. 创建Handler(句柄)对象 ==> 如何处理日志信息
3. 创建Formatter对象 ==> 日志信息的格式
4. 将Formatter传递给Handler，将Handler传递给logger
5. 调用logger方法，如logger.info, logger.error等
"""

import logging
import os
from logging.handlers import RotatingFileHandler
from logging.handlers import TimedRotatingFileHandler
from typing import Optional

FORMAT = "%(asctime)s - %(levelname)s - %(message)s"


def ensure_dir(filename: str) -> None:
    if not filename.endswith(".log"):
        raise ValueError("log file must have postfix '.log'")
    dirname = os.path.dirname(os.path.abspath(filename))
    os.makedirs(dirname, exist_ok=True)


def get_loglevel(level: str) -> int:
    loglevel = getattr(logging, level.upper(), None)
    if loglevel is None:
        raise ValueError(f"invalid log level '{level}'")
    return loglevel


def setup_stream_handler(level: str = "info") -> logging.StreamHandler:
    handler = logging.StreamHandler()
    handler.setLevel(get_loglevel(level))
    handler.setFormatter(logging.Formatter(FORMAT))
    return handler


def setup_file_handler(level: str = "info",
                       filename: Optional[str] = "log.log",
                       max_bytes: int = 10240,
                       backup: int = 10) -> RotatingFileHandler:
    handler = RotatingFileHandler(
        filename, maxBytes=max_bytes, backupCount=backup)
    handler.setLevel(get_loglevel(level))
    handler.setFormatter(logging.Formatter(FORMAT))
    return handler


def setup_logger(to_console: bool = True,
                 to_file: bool = True,
                 level_console: str = "info",
                 level_file: str = "info",
                 filename: str = "log.log",
                 max_bytes: int = 1024000,
                 backup: int = 10) -> logging.Logger:
    """创建自定义Logger对象，允许将日志输出到终端或文件，日志文件默认
    根据大小进行滚动

    Args:
        to_console (bool, optional): 是否输出到终端.
        to_file (bool, optional): 是否输出到文件.
        level_console (str, optional): 输出到终端的日志级别.
        level_file (str, optional): 输出到文件的日志级别.
        filename (str, optional): 日志文件路径.
        max_bytes (int, optional): 文件大小超过阈值后自动滚动.
        backup (int, optional): 轮换日志文件的数量.

    Returns:
        logging.Logger
    """
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    if to_console:
        logger.addHandler(setup_stream_handler(level_console))

    if to_file:
        ensure_dir(filename)
        logger.addHandler(setup_file_handler(
            level_file, filename, max_bytes, backup))

    return logger


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


# class CustomLogger:
#     """便捷自定义logger

#     根据参数创建至多两个句柄: 控制台句柄和文件句柄，后者默认会根据时间滚动，
#     默认在本地时间午夜自动创建新日志文件。
    
#     Attributes:
#         name(str): logger名字，建议使用当前模块的名字(__name__)
#         to_console(bool): 是否把信息输出到控制台
#         to_file(bool): 是否把信息输出到日志文件
#         filename(str): 日志文件名称，务必先创建存储文件的文件夹
#         level_console: 输出到控制台的日志信息的紧急程度
#         level_file: 输出到文件的日志信息的紧急程度
#         format_console: 输出到控制台的信息的格式
#         format_file: 输出到日志文件的信息的格式
#     """
#     def __init__(self, name, to_console=True, to_file=False,
#                  filename=None, level_console=logging.INFO,
#                  level_file=logging.WARNING, format_console=None,
#                  format_file=None):
#         self.to_console = to_console
#         self.to_file = to_file
#         self.filename = filename
#         self.level_console = level_console
#         self.level_file = level_file
#         self.format_console = format_console
#         self.format_file = format_file

#         self.logger = logging.getLogger(name)
#         # 必须将logger的level设成最低级，才能为不同的handlers设置不同级别的level
#         self.logger.setLevel(logging.DEBUG)

#     def _get_console_formatter(self):
#         if self.format_console is None:
#             self.format_console = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
#         return logging.Formatter(self.format_console)

#     def _get_file_formatter(self):
#         if self.format_file is None:
#             self.format_file = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
#         return logging.Formatter(self.format_file)

#     def _add_console_handler(self):
#         handler = logging.StreamHandler()
#         handler.setLevel(self.level_console)
#         handler.setFormatter(self._get_console_formatter())
#         self.logger.addHandler(handler)

#     def _add_file_handler(self):
#         if self.filename is None:
#             raise Exception("Filename missing when setting FileHandler for logger")
#         handler = TimedRotatingFileHandler(self.filename, when="midnight")
#         handler.setLevel(self.level_file)
#         handler.setFormatter(self._get_file_formatter())
#         self.logger.addHandler(handler)

#     def get_logger(self):
#         if self.to_console:
#             self._add_console_handler()
#         if self.to_file:
#             self._add_file_handler()
#         return self.logger


# if __name__ == "__main__":
#     logger = CustomLogger(__name__).get_logger()
#     logger.info("log some information")