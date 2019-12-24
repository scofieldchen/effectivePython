"""
用pytest进行测试

测试的经典步骤：
1. 明确要测试的内容：函数，类属性/方法，单元测试或整合测试
2. 自定义输入
3. 写测试代码，一般会借助于test runner, 如unittest或pytest
4. 将结果与预期相比较
"""

def func(x, y):
    return x + y


def test_func():
    x, y = 1, 3
    # assert func(x, y) == 4  # success
    assert func(x, y) == 5  # fail
