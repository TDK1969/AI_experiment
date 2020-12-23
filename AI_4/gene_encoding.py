import random


def gene_encoding(pop_size, chrom_length):
    """

    基因编码函数
    :param pop_size: 种群数量
    :param chrom_length: 染色体长度
    :return: 生成的初始种群
    """

    pop = []  # 2d
    for i in range(pop_size):
        temp = []
        for j in range(chrom_length):
            temp.append(random.randint(0, 1))
            # 每一位都随机位0或1
        pop.append(temp)
        # 将生成的一个基因加入种群
    return pop[:]
