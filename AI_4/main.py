import numpy as np
import matplotlib.pyplot as plt
import math

from cal_fit_value import cal_fit_value
from selection import selection
from crossover import crossover
from mutation import mutation
from best import best
from gene_encoding import gene_encoding
import settings


def b2d(b, max_value, chrom_length):
    t = 0
    for j in range(len(b)):
        t += b[j] * (math.pow(2, j))
    t = t * max_value / (math.pow(2, chrom_length) - 1)
    return t


# 进化代数
generations = settings.generations
# 种群数量
pop_size = settings.pop_size
# 基因中允许出现的最大值
max_value = settings.max_value
# 染色体长度
chrom_length = settings.chrom_length
# 交配概率
pc = settings.pc
# 变异概率
pm = settings.pm

results = []  # 2d 存储每一代的最优解，[[best_fit, best_gene_encoding_dec]]
fit_value = []  # 个体适应度

pop = gene_encoding(pop_size, chrom_length)
best_individual, best_fit = 0, 0

for i in range(generations):
    fit_value = cal_fit_value(pop, chrom_length, max_value)  # 个体评价
    best_individual, best_fit = best(pop, fit_value)  # 第一个存储最优的解, 第二个存储最优基因
    results.append([best_fit, b2d(best_individual, max_value, chrom_length)])
    pop = selection(pop, fit_value)  # 新种群复制
    crossover(pop, pc)  # 交配
    mutation(pop, pm)  # 变异

results = results[1:]
results.sort()
best_x = results[-1][1]
best_y = results[-1][0]
print('y=10sin(5x)+7|x-5|+10')
print(best_x, best_y)
print(best_individual)
print(best_fit)

x = np.arange(-0.1, 10.1, 0.1)
y = 10 * np.sin(5 * x) + 7 * abs(x - 5) + 10
plt.plot(x, y)
for res in results:
    plt.plot(res[1], res[0], marker='^', color='green')
plt.plot(best_x, best_y, marker='o', color='red')
plt.title("y=10sin(5x)+7|x-5|+10")
plt.xlabel("x∈[0,10]")
plt.ylabel("y")
plt.show()
