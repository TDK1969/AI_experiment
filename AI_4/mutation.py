# 0.0 coding:utf-8 0.0
# 基因突变

import random


def mutation(pop, pm):
    """
    基因突变
    :param pop: 种群
    :param pm: 突变概率
    :return: 无返回值，直接在pop上操作
    """
    px = len(pop)
    py = len(pop[0])
    
    for i in range(px):
        r = random.random()
        print(r)
        if r < pm:
            mpoint = random.randint(0, py-1)  # 随机产生变异位点
            # 进行变异
            # 或者可以写成 pop[i][mpoint] = !pop[i][mpoint]
            if pop[i][mpoint] == 1:
                pop[i][mpoint] = 0
            else:
                pop[i][mpoint] = 1