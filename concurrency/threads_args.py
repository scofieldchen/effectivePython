import threading

"""
可以将参数传递给在子线程中运行的函数，参数以元组的形式
传递。
"""

def worker(num):
    print("argument = %d" % num)


threads = []
for i in range(5):
    t = threading.Thread(target=worker, args=(i,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()