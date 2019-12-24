"""
测试代码会引发特定异常
"""

import pytest

class CustomException(Exception):
    pass


def func():
    raise CustomException()


def test_func():
    with pytest.raises(CustomException):
        func()