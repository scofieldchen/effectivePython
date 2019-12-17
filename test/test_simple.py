def my_sum(x, y):
    return x + y


def test_sum():
    x, y = 1, 3
    assert my_sum(x, y) == 4
