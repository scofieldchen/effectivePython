import time
import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s-%(threadName)s-%(levelname)s-%(message)s",
    filename="./test_script.log",
    datefmt="%Y-%m-%d %H:%M:%S"
)


if __name__ == "__main__":
    cnt = 0
    while cnt < 20:
        logging.info("script running")
        cnt += 1
        time.sleep(1)