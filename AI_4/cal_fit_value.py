# 0.0 coding:utf-8 0.0
# 解码并计算值

import math


def decode_chrom(pop, chrom_length):
    temp = []
    for i in range(len(pop)):
        t = 0
        for j in range(chrom_length):
            t += pop[i][j] * (math.pow(2, j))
        temp.append(t)
    return temp


def cal_fit_value(pop, chrom_length, max_value):
    temp1 = []
    obj_value = []
    temp1 = decode_chrom(pop, chrom_length)
    for a in temp1:
        print(a)
    print()
    for i in range(len(temp1)):
        x = temp1[i] * max_value / (math.pow(2, chrom_length) - 1)
        print(x)
        f = 10 * math.sin(5 * x) + 7 * abs(x - 5) + 10
        obj_value.append(f)
    return obj_value