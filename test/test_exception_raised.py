import pytest


def my_division(x, y):
    return x / y


def test_division():
    x, y = 1, 0
    with pytest.raises(ZeroDivisionError):
        my_division(x, y)