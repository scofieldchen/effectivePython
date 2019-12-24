"""
我们可以把很多测试封装在一个类中，pytest不要求测试类继承任何对象，只要求类名
以'Test'开头，测试方法以'test_'开头即可。
"""


class TestClass:

    def test_one(self):
        assert sum([1, 2, 3]) == 6

    def test_two(self):
        assert abs(-2) == 2