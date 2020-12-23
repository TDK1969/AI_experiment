# 0.0 coding:utf-8 0.0
# 解码并计算值

import math


def decode_chrom(pop, chrom_length):
    """
    基因解码
    :param pop: 种群的所有基因
    :param chrom_length: 染色体长度
    :return: 解码的基因的列表
    """
    temp = []
    for i in range(len(pop)):
        t = 0
        for j in range(chrom_length):
            t += pop[i][j] * (math.pow(2, j)) # 二进制转十进制
        temp.append(t)
    return temp


def cal_fit_value(pop, chrom_length, max_value):
    """
    对群体进行评价
    :param pop: 种群基因
    :param chrom_length:染色体长度
    :param max_value: 基因允许的最大值
    :return:
    """
    temp1 = []
    obj_value = []
    temp1 = decode_chrom(pop, chrom_length) # 对种群基因进行解码
    for a in temp1:
        print(a)
    print()
    for i in range(len(temp1)):
        x = temp1[i] * max_value / (math.pow(2, chrom_length) - 1)
        # 因为基因可能并不能取到0~2的染色体长度次方-1所有的值，所以上面需要调整权值
        print(x)
        f = 10 * math.sin(5 * x) + 7 * abs(x - 5) + 10 # 根据函数计算适应度
        obj_value.append(f)
    return obj_value