"""
假设以下问题：

存在一份巨大的log文件，包含数千万行内容，需要根据条件筛选一部分内容，并存储到另一份文件，
有两种解决方案：第一，读取所有行并存储在列表中，然后再挑选符合条件的行；第二，创建包含
所有行的迭代器，每次处理一行；第一种方法会占用大量内存，第二种方法不占用内存，每次仅
处理一个元素，处理完毕后迭代器中的所有元素将被耗尽。

如果并不真正需要列表，元素或字典来存储数据，而只是从一个序列汇总，筛选，转换元素，生成器
表达式是最有效的。
"""

## 生成一份log文件
# import time
# import random
# from custom_logger import setup_logger

# logger = setup_logger("test", filename="large_log_file.log")

# cnt = 0
# rows = 1000
# levels = ["info", "warning", "error"]
# while cnt < 1000:
#     level = random.sample(levels, k=1)[0]
#     if level == "info":
#         logger.info("this is info message")
#     elif level == "warning":
#         logger.warning("this is warning message")
#     elif level == "error":
#         logger.error("this is error message")
#     cnt += 1
#     time.sleep(0.01)


## 使用生成器表达式遍历一份巨大的log文件，打印所有的error行
filename = "./large_log_file.log"

with open(filename, "r") as file:
    # 生成器表达式，返回迭代器，每次仅处理一个元素，节省内存
    error_rows = (row for row in file if "ERROR" in row)
    for row in error_rows:
        print(row)