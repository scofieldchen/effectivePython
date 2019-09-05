## iterable: 可迭代对象
## 可迭代对象是可以用'for loop'遍历的对象，例如字符串，列表，元组等
example_iterable = [1, 2, 3, 4, 5]
for item in example_iterable:
    print(item)

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


## for loop的实现原理：基于iterator

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
