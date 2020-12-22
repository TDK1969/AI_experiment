import numpy as np
import matplotlib.pyplot as plt
import math

from cal_fit_value import cal_fit_value
from selection import selection
from crossover import crossover
from mutation import mutation
from best import best
from gene_encoding import gene_encoding


def b2d(b, max_value, chrom_length):
    t = 0
    for j in range(len(b)):
        t += b[j] * (math.pow(2, j))
    t = t * max_value / (math.pow(2, chrom_length) - 1)
    return t


# 种群数量
pop_size = 6
# 基因中允许出现的最大值
max_value = 10
# 染色体长度
chrom_length = 10
# 交配概率
pc = 0.6
# 变异概率
pm = 0.1

results = []  # 2d 存储每一代的最优解，[[best_fit, best_gene_encoding_dec]]
fit_value = []  # 个体适应度

pop = gene_encoding(pop_size, chrom_length)
print('-'*20, "gene_encoding", '-'*20)
for a in pop:
    print(a)
print()

fit_value = cal_fit_value(pop, chrom_length, max_value)  # 个体评价
print('-'*20, "cal_fit_value", '-'*20)
for b in fit_value:
    print(b)
print()

best_individual, best_fit = best(pop, fit_value)  # 第一个存储最优的解, 第二个存储最优基因
print('-'*20, "best", '-'*20)
print(best_individual)
print(best_fit)
print()

results.append([best_fit, b2d(best_individual, max_value, chrom_length)])

pop = selection(pop, fit_value)  # 种群选择
print('-'*20, "selection", '-'*20)
for c in pop:
    print(c)
print()

crossover(pop, pc)  # 交配
print('-'*20, "crossover", '-'*20)
for d in pop:
    print(d)
print()


mutation(pop, pm)  # 变异
print('-'*20, "mutation", '-'*20)
for e in pop:
    print(e)
print()

results = results[:]
results.sort()
best_x = results[-1][1]
best_y = results[-1][0]
print('y = 10 * math.sin(5 * x) + 7 * abs(x - 5)+10')
print(best_x, best_y)
print(best_individual)
print(best_fit)

x = np.arange(-0.1, 10.1, 0.1)
y = 10 * np.sin(5 * x) + 7 * abs(x - 5) + 10
plt.plot(x, y)
plt.plot(best_x, best_y, marker='o')
plt.title("y=10sin(5x)+7|x-5|+10")
plt.xlabel("x∈[0,10]")
plt.ylabel("y")
plt.show()
