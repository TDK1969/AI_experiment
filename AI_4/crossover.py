# 0.0 coding:utf-8 0.0
# 交配

import random


def crossover(pop, pc):
    """
    交配
    :param pop: 种群
    :param pc: 交叉概率
    :return: 无返回值，直接在pop上操作
    """
    pop_len = len(pop)
    for i in range(0, pop_len, 2):  # 这里为什么不随机选两个？
        r = random.random()  # 随机产生0~1的数
        print(r)
        if r < pc:  # 满足交叉的概率，进行交叉
            cpoint = random.randint(0, len(pop[0]))  # 随机产生交换位点
            temp1 = []
            temp2 = []

            # 利用extend方法和列表切片，组成新的两个基因
            temp1.extend(pop[i][0:cpoint])
            temp1.extend(pop[i+1][cpoint:len(pop[i])])
            temp2.extend(pop[i+1][0:cpoint])
            temp2.extend(pop[i][cpoint:len(pop[i])])
            # 交换形成的新基因返回种群
            pop[i] = temp1
            pop[i+1] = temp2
