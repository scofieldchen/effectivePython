import time
import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s-%(threadName)s-%(levelname)s-%(message)s",
    filename="./test_script.log",
    datefmt="%Y-%m-%d %H:%M:%S"
)


if __name__ == "__main__":
    while True:
        logging.info("script running")
        time.sleep(1)