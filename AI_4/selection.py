# 0.0 coding:utf-8 0.0
# 选择

import random


def sum(fit_value):
    """
    计算适应度之和
    :param fit_value: 种群适应度
    :return: 种群适应度之和
    """
    total = 0
    for v in fit_value:
        total += v
    return total


def accum(fit_value):
    """
    计算累计概率
    :param fit_value: 百分比形式的种群适应度
    :return: 累计概率
    """
    for i in range(1, len(fit_value) - 1):
        fit_value[i] += fit_value[i - 1] # 前i项的和赋值给fit_value[i]
        fit_value[-1] = 1 # 最后一项为1


def selection(pop, fit_value):
    """
    选择
    :param pop:原来的种群
    :param fit_value:种群各基因的适应度
    :return:选择后的新种群
    """
    new_fit_value = []
    # 适应度总和
    total_fit = sum(fit_value)
    for i in range(len(fit_value)):
        new_fit_value.append(fit_value[i] / total_fit)
        # 将适应度转换为百分比
    # 打印累加之前的new_fit_value
    for a in new_fit_value:
        print(a)
    print()
    # 计算累计概率
    accum(new_fit_value)
    # 打印累加之前后的new_fit_value
    for a in new_fit_value:
        print(a)
    print()

    random_p = []
    for i in range(len(pop)):
        # 随机产生len(pop)个0~1的小数，加入random_p中
        random_p.append(random.random())
    for p in random_p:
        print(p)
    print()

    new_pop = []
    # 转轮盘选择法
    for i in range(len(random_p)):
        for j in range(len(new_fit_value)):
            if random_p[i] <= new_fit_value[j]: # 看随机数落入了哪个区间
                new_pop.append(pop[j]) # 将选中该的基因加入新种群
                print(j + 1)
                break
    for n in new_pop:
        print(n)

    return new_pop
