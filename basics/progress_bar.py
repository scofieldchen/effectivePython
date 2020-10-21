# 使用tqdm创建进度条

import time

from tqdm import tqdm


def progress_bar_iterable():
    # 将一个可迭代对象传递给tqdm(iterable)函数，自动创建进度条
    for _ in tqdm(range(20)):
        time.sleep(0.1)


def progress_bar_iterable_2():
    # 创建并管理pbar对象，例如添加一些描述性文字
    pbar = tqdm(range(20))
    for char in pbar:
        time.sleep(0.1)
        pbar.set_description(f"processing {char}")


def progress_bar_manual():
    # 手动控制进度条的更新进度
    # 总进度为100，分10次更新，每次更新10%
    # 在这种情况下最好使用上下文管理器，自动管理进度条的创建和退出
    with tqdm(total=100) as pbar:
        for _ in range(10):
            time.sleep(1)
            pbar.update(10)


# progress_bar_iterable()
# progress_bar_iterable_2()
progress_bar_manual()
