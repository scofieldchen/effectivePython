"""
可迭代对象，迭代器，for loop，迭代器协议

https://towardsdatascience.com/python-basics-iteration-and-looping-6ca63b30835c
"""

## ----------------------------------------------------------- ##
## iterable: 可迭代对象
## 可迭代对象是可以用'for loop'遍历的对象，例如字符串，列表，元组等
example_iterable = [1, 2, 3, 4, 5]
for item in example_iterable:
    print(item)


## ----------------------------------------------------------- ##
## iterator: 迭代器
## 迭代器是管理数据流(stream of data)的对象
## iter(iterable) ==> 创建一个iterator
iterator = iter(example_iterable)
iterator

# 调用next(iterator)能够遍历可迭代对象中的每一个元素
# 从迭代器中取出一个元素后它就消失了
next(iterator)
next(iterator)
next(iterator)
next(iterator)
next(iterator)
next(iterator)  # 迭代器没有元素后调用next()会引发'StopIteration'异常


## ----------------------------------------------------------- ##
## for loop的实现原理：基于iterator
## step1: 调用iter()，创建迭代器
## step2: 不断调用next()返回下一个元素
## step3: 耗尽所有元素后处理StopIteration异常


def custom_loop(iterable, callback):
    """利用迭代器遍历可迭代对象
    callback: 处理元素的函数
    """
    # 用iter()创建一个迭代器
    iterator = iter(iterable)

    # 不断调用next()从迭代器中取出元素，穷尽所有元素后退出
    while True:
        try:
            item = next(iterator)
        except StopIteration:
            break
        else:
            callback(item)

# 遍历一个可迭代对象
example_iterable = {1, 2, 3, 4, 5}
custom_loop(example_iterable, print)


## ----------------------------------------------------------- ##
## 自定义迭代器
## 迭代器协议(iterator protocol) ==> 创建迭代器的规则
## 要求实现两个魔术方法：__iter__, __next__
## __iter__，返回迭代器自身，在外部调用iter()时被执行
## __next__，指向可迭代对象的下一个元素，在外部调用next()时执行，元素被耗尽时引发StopIteration异常

class GenerateNumber:

    def __init__(self, min_value, max_value):
        self.current = min_value
        self.max_value = max_value

    def __iter__(self):
        # 返回自身即可
        return self

    def __next__(self):
        # 返回下一个元素
        # 耗尽所有元素后引发StopIteration异常
        if self.current > self.max_value:
            raise StopIteration
        else:
            self.current += 1
            return self.current - 1

numbers = GenerateNumber(0, 3)
type(numbers)
next(numbers)

list(GenerateNumber(1, 10))

for i in GenerateNumber(1,5):
    print(i)


## 生成器(Generator)和生成器表达式(Generator Expression)

## 生成器：包含yield关键字的函数，负责‘生产’一系列的值，这些值可以用循环来遍历，
## 也可以用next()取出

def generate_numbers(min_value, max_value):
    while min_value <= max_value:
        yield min_value
        min_value += 1

numbers = generate_numbers(1, 5)
type(numbers)

for num in numbers:
    print(num)        

list(generate_numbers(1, 10))

next(numbers)



