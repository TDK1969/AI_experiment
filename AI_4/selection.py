# 0.0 coding:utf-8 0.0
# 选择

import random


def sum(fit_value):
    total = 0
    for v in fit_value:
        total += v
    return total


def accum(fit_value):
    for i in range(1, len(fit_value) - 1):
        fit_value[i] += fit_value[i - 1]
        fit_value[-1] = 1


def selection(pop, fit_value):
    new_fit_value = []
    # 适应度总和
    total_fit = sum(fit_value)
    for i in range(len(fit_value)):
        new_fit_value.append(fit_value[i] / total_fit)
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
        random_p.append(random.random())
    for p in random_p:
        print(p)
    print()

    new_pop = []
    # 转轮盘选择法
    for i in range(len(random_p)):
        for j in range(len(new_fit_value)):
            if random_p[i] <= new_fit_value[j]:
                new_pop.append(pop[j])
                print(j + 1)
                break
    for n in new_pop:
        print(n)

    return new_pop
