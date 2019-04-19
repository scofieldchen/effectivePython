import threading


"""
如何使用线程？

创建Thread对象，提供target函数，调用start和join方法。
start ==> 启动线程
join ==> 等待子线程结束并回归主线程

线程常用于处理密集型IO任务。
"""
def worker():
    # 线程常用于处理密集型IO任务
    print("handle I/O tasks")


threads = []
for _ in range(5):
    t = threading.Thread(target=worker)
    threads.append(t)
    t.start()

for t in threads:
    t.join()