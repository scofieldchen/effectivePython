"""
deque：双端队列，能够从两端进行操作。
"""

from collections import deque
import time
import random


## 创建固定长度的双端队列，当有新记录入队时会自动剔除最老的那条记录
q = deque(maxlen=3)
for i in range(3):
    q.append(i)
print(q)

q.append(3)  # 从右端入队，跟list结果一致，从左端入队使用append_left
print(q)


## 如果不设定长度，就成为无界限的队列，可以在两边添加和删除元素
q = deque()
q.append("kobe")
q.append("iris")
q.append("bob")
print(q)
q.append("tracy")  # 从右端添加
print(q)
q.appendleft("mike")  # 从左端添加
print(q)
q.pop()  # 从右端删除
print(q)
q.popleft()  # 从左端删除
print(q)


## 应用：保留最新的n个元素
## 假设一个接受实时数据的程序，保留最新的5个数据
q = deque(maxlen=5)
cnt = 0
while cnt < 100:
    time.sleep(0.2)
    x = random.randint(10, 20)
    q.append(x)
    print("x = %d, q = %s" % (x, str(q)))
    cnt += 1

