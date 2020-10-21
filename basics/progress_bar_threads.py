# 在多线程的条件下使用tqdm创建进度条

import time
import random
from concurrent.futures import ThreadPoolExecutor, as_completed

from tqdm import tqdm


def process_data(x):
    time.sleep(random.randint(1, 2))
    return x ** 2


numbers = list(range(10))
results = []
with ThreadPoolExecutor(max_workers=3) as executor:
    futures = [executor.submit(process_data, x=x) for x in numbers]
    # 在多线程的条件下，直接传递futures给tqdm()函数是错误的，以下代码都无法工作
    # for f in as_completed(tqdm(futures)):  # 马上显示100%进度
        # results.append(f.result())
    # for f in tqdm(as_completed(futures)):  # 不显示进度条
        # results.append(f.result())

    # 正确的代码是：先创建进度条对象，没完成一个任务，调用update()更新
    with tqdm(total=len(numbers)) as pbar:
        for f in as_completed(futures):
            results.append(f.result())
            pbar.update()

print(results)
