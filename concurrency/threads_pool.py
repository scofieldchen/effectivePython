"""
线程池(threadPool)提供管理多个线程的自动化方案，当需要执行多个IO任务时
非常有用，它不需要程序员分别管理单个线程。

concurrent.futures提供ThreadPoolExecutor类，这是实现线程池的最优方法。
"""

from concurrent.futures import ThreadPoolExecutor,as_completed
from lxml import html
import requests


def thread_pool_basic():
    """
    使用线程池的最简单方法：
    1. 创建线程池对象
    2. 定义worker函数，提交至线程池
    3. 获取结果
    """

    # worker函数
    def cal_square(x):
        return(x**2)
    
    # 实例化ThreadPoolExecutor类(理解为线程池对象)
    # max_workers是包含的线程数
    executor = ThreadPoolExecutor(max_workers=3)

    # 调用executor的submit方法：将任务"提交"至线程池
    # submit方法返回future对象(理解为已完成任务)
    future_list = []
    for i in range(3):
        # 一旦提交，任务会在子线程中自动执行
        # 可以向worker函数传递参数(元组)
        future = executor.submit(cal_square, i)
        future_list.append(future)

    # 调用future的result方法会得到计算结果
    for future in future_list:
        print(future.result())


def thread_pool_context_manager():
    """
    使用上下文管理器中管理线程池。
    上下文管理器(context manager)用于处理代码块的准备和收尾工作，原理
    类似于try/finally。
    常见情形有：
    1. 操作文件：获得文件句柄，执行代码后释放句柄。
    2. 连接数据库：获得连接对象，执行代码后关闭连接。
    3. 多线程：获取互斥锁，执行代码后释放互斥锁。
    
    接下来将使用爬取网页的案例作为示范，多线程也经常用于处理密集型
    IO任务，例如同时爬取多个网站的内容。
    """
    urls = [
        "https://realpython.com/",
        "https://pymotw.com/3/",
        "https://www.earnforex.com/",
        "https://www.tradingview.com/",
        "https://this-is-fake-domain.com"  # 该结果会失败
    ]

    def scrape_web(url):
        """
        爬取网页内容的简单函数
        """
        page = requests.get(url)
        tree = html.fromstring(page.content)
        return(tree)

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(scrape_web, url) for url in urls]
        # as_completed: 获得已完成的future
        for future in as_completed(futures, timeout=30):
            try:
                data = future.result()
            except Exception as e:
                print(e)
            else:
                print(data)


def thread_pool_map():
    """
    executor类有一个广泛使用的map方法，将worker函数映射到一系列
    参数，最终返回一个生成器对象。
    """
    def cal_square(x):
        return(x**2)

    inputs = list(range(5))
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = executor.map(cal_square, inputs)
    
    #print(list(results))
    for result in results:
        print(result)


if __name__ == "__main__":

    #thread_pool_basic()
    #thread_pool_context_manager()
    thread_pool_map()