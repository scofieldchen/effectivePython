"""
生成器(generator)：包含yield的函数。

为什么使用生成器？
1. 实现惰性运算，不占用内存，处理大型数据集有优势。
2. 语法简单，容易理解。

教程：
1. https://realpython.com/introduction-to-python-generators/
2. https://anandology.com/python-practice-book/iterators.html
3. http://www.dabeaz.com/generators/
4. https://dbader.org/blog/python-iterator-chains

"""

## 如何使用生成器
## ------------------------------------------------------- ##

# 定义一个包含yield的函数（用yield取代return）
def my_gen(nums):
    """求nums中所有元素的平方"""
    print("start computing")
    for n in nums:
        yield(n ** 2)

# 调用my_gen不会打印'start computing'，因为它是生成器，
# 返回生成器对象，由这个对象控制实际运算
res = my_gen([1, 2, 3, 4, 5])
print(type(res))

# 调用next方法，让生成器执行运算并返回结果
for _ in range(5):
    print(next(res))


## 生成器表达式(generator expression)
## ------------------------------------------------------- ##

# 生成器表达式类似列表推导，列表推导使用'[]'，生成器表达式使用'()'
# 表达式返回生成器对象，节省很多内存，是生成器被广泛使用的原因
nums = [1, 2, 3, 4, 5]
res = (x**2 for x in nums)  # 使用'()'而不是'[]'
print(res)
for i in res:
    print(i)

# 对比生成器表达式和列表推导对内存的占用
import sys

l = [x for x in range(1000000) if x % 2 == 0]  # 列表推导返回列表，存储在内存中
print(sys.getsizeof(l))
print(sum(l))

g = (x for x in range(1000000) if x % 2 == 0)  # 返回生成器，不占用内存
print(sys.getsizeof(g))
print(sum(g))

del l

# 对比生成器表达式和列表推导的计算时间
# 生成器表达式消耗更多计算时间，但节省内存的优势完全可以弥补短板
import cProfile

cProfile.run('sum([x for x in range(1000000) if x % 2 == 0])')

cProfile.run('sum((x for x in range(1000000) if x % 2 == 0))')


## 案例
## ------------------------------------------------------- ##
import sys

lines = []
with open("test_file.txt") as f:
    for line in f:
        lines.append(line)

sys.getsizeof(lines)

lines[0]

for i in lines[0]:
    print(i)



