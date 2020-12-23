# 0.0 coding:utf-8 0.0
# 找出最优解和最优解的基因编码


def best(pop, fit_value):
    """
    找出最优解和最优解的基因编码
    :param pop: 种群基因
    :param fit_value: 种群基因的适应值
    :return: 由最优基因和最优解组成的列表
    """
    px = len(pop)
    best_individual = []
    best_fit = fit_value[0] # 最优解初始化位第一个基因的适应度
    for i in range(1, px):
        # 遍历fit_value列表，寻找最大值
        if fit_value[i] > best_fit:
            best_fit = fit_value[i]
            best_individual = pop[i] # 找到最大值时同时将对应的基因赋给最优基因
    return [best_individual, best_fit]