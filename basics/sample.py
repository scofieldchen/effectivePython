"""
由subprocess启动脚本
"""

import time
import sys
import logging

logging.basicConfig(
    level=logging.INFO,
    filename="/home/scofield/python/basics/sample.log",
    format="%(asctime)s - %(levelname)s - %(message)s"
)


if __name__ == "__main__":
    arg = sys.argv[1]
    while True:
        logging.info("%s is running" % arg)
        time.sleep(1)