"""
如何终止进程？

1. Process.is_alive() ==> 判断进程是否在运行
2. Process.terminate() ==> 终止进程
3. Process.exitcode ==> 退出码

ExitCode的可能值：

1. ExitCode == 0: 没有错误
2. ExitCode > 0: 进程遇到错误并退出
3. ExitCode < 0: 进程被外部信号杀死
"""

import time
import logging
import multiprocessing

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(processName)s - %(levelname)s - %(message)s"
)


def worker():
    while 1:
        logging.info("doing some work")
        time.sleep(2)


p = multiprocessing.Process(target=worker)
logging.info(f"Before start: {str(p)} alive={p.is_alive()}")

p.start()
logging.info(f"Start process: {str(p)} alive={p.is_alive()}")

time.sleep(5)

## 调用terminate不代表进程马上退出，调用terminate后再调用is_alive有时候会显示进程仍在运行
## 这可能是因为进程还没有完全结束的缘故，这时候状态码也为None。
## 要保证进程完全退出，有两种处理方法：
## 1. 调用terminate后主动等待一段时间，如0.5秒，再调用is_alive确认。
## 2. 调用terminate后再调用join，确保子进程回归主进程。
## 第二种方法更有效率。
p.terminate()
# time.sleep(0.5)
logging.info(f"Terminate process: {str(p)} alive={p.is_alive()} exit_code={str(p.exitcode)}")

p.join()  # 确保子进程回归父进程
logging.info(f"Join process: {str(p)} alive={p.is_alive()} exit_code={str(p.exitcode)}")