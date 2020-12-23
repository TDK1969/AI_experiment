import numpy as np


def F(x, y):
    """
    计算函数
    :param x:
    :param y:
    :return:
    """
    ans = -(x**2+3*y**4-0.2*np.cos(3*np.pi*x) - 0.4*np.cos(4*np.pi*y)+0.6)
    return ans
