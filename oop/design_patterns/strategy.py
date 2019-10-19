"""
策略模式(Strategy Pattern)

对于同一个问题，有多个解决办法，用一系列函数(类)分别实现这些方法，它们接收
相同的参数，返回相同格式的结果。客户端程序根据场景选择特定的算法并计算结果。
"""

import numpy as np


class Numbers:
    
    def __init__(self, nums):
        self.nums = nums

    def calculate(self, method):
        """
        method(callback): 实现不同计算方法的函数
        """
        return method(self.nums)


def myMean(nums):
    return np.mean(nums)


def mySum(nums):
    return np.sum(nums)


if __name__ == "__main__":

    nums = [1, 2, 3, 4, 5]
    numbers = Numbers(nums)
    print(numbers.calculate(myMean))
    print(numbers.calculate(mySum))