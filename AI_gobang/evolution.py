from settings import ROW, COLUMN
import random
import copy
import time
import sys
from evaluate import *
import math

generations = 100
pop_size = 50
max_value = 15
chrom_length = 8
pc = 0.6
pm = 0.1

class evolution():
    def __init__(self):
        self.results = []
        self.pop_size = pop_size
        self.generations = generations
        self.chrom_length = chrom_length
        self.pc = pc
        self.pm = pm
        self.pop = []


    def GetBestPos(self, Databoard, player):
        BeginTime = time.time()
        self.Databoard = copy.deepcopy(Databoard)

        if player:
            self.ComRole = 1
            self.HumRole = 2
        else:
            self.ComRole = 2
            self.HumRole = 1

        self.gene_encoding()

        best_individual, best_fit = 0, 0

        for i in range(self.generations):
            fit_value = self.cal_fit_value()
            best_individual, best_fit = self.best(fit_value)
            self.results.append([best_fit, self.transform(best_individual)])
            self.pop = self.selection(fit_value)
            self.crossover()
            self.mutation()

        self.results = self.results[1:]
        self.results.sort()
        best_x = self.results[-1][1][0]
        best_y = self.results[-1][1][1]
        EndTime = time.time()
        UsedTime = EndTime - BeginTime
        return best_x, best_y, UsedTime

    def gene_encoding(self):
        self.pop = []
        for i in range(self.pop_size):
            temp = []
            for j in range(self.chrom_length):
                temp.append(random.randint(0, 1))
            self.pop.append(temp)

    def TDK_evaluate(self, x, y):
        list1 = []
        list2 = []
        list3 = []
        list4 = []

        for tmp in range(-4, 5):
            i = x + tmp
            j = y + tmp
            if i < 0 or i > 14:
                list1.append(-1)
            else:
                list1.append(self.Databoard[i][y])
            if j < 0 or j > 14:
                list2.append(-1)
            else:
                list2.append(self.Databoard[x][j])
            if i < 0 or j < 0 or i > 14 or j > 14:
                list3.append(-1)
            else:
                list3.append(self.Databoard[i][j])
            k = y - tmp
            if i < 0 or k < 0 or i > 14 or k > 14:
                list4.append(-1)
            else:
                list4.append(self.Databoard[i][k])
        #print(1)
        #playerValue = value_point(player, enemy, list1, list2, list3, list4)
        #enemyValue = value_point(enemy, player, list1, list2, list3, list4)
        value = TDK_value(self.ComRole, self.HumRole, list1, list2, list3, list4)

        return value

    def decode_chrom(self):
        temp = []
        for i in range(len(self.pop)):
            x = 0
            y = 0

            for j in range(4):
                x += self.pop[i][j] * (math.pow(2, j))
                y += self.pop[i][j + 4] * (math.pow(2, j))
            x = int(x)
            y = int(y)
            temp.append([x, y])
        return temp

    def cal_fit_value(self):
        obj_value = []
        temp = self.decode_chrom()
        for i in range(len(temp)):
            value = 0
            x = temp[i][0]
            y = temp[i][1]
            if x > 14 or y > 14 or self.Databoard[x][y] != 0:
                value = 0
            else:
                self.Databoard[x][y] = self.ComRole
                value = self.TDK_evaluate(x, y)
                self.Databoard[x][y] = 0
            obj_value.append(value)
        return obj_value

    def best(self, fit_value):
        """
        找出最优解和最优解的基因编码
        :param pop: 种群基因
        :param fit_value: 种群基因的适应值
        :return: 由最优基因和最优解组成的列表
        """
        px = len(self.pop)
        best_individual = self.pop[0]
        best_fit = fit_value[0]  # 最优解初始化位第一个基因的适应度
        for i in range(1, px):
            # 遍历fit_value列表，寻找最大值
            if fit_value[i] > best_fit:
                best_fit = fit_value[i]
                best_individual = self.pop[i]  # 找到最大值时同时将对应的基因赋给最优基因
        return [best_individual, best_fit]

    def transform(self, individual):
        x, y = 0, 0
        for j in range(4):
            x += individual[j] * (math.pow(2, j))
            y += individual[j + 4] * (math.pow(2, j))
            x = int(x)
            y = int(y)
        return [x, y]

    def selection(self, fit_value):
        new_fit_value = []
        # 适应度总和
        total_fit = self.sum(fit_value)
        for i in range(len(fit_value)):
            new_fit_value.append(fit_value[i] / total_fit)
            # 将适应度转换为百分比
        # 计算累计概率
        self.accum(new_fit_value)

        random_p = []
        for i in range(len(self.pop)):
            # 随机产生len(pop)个0~1的小数，加入random_p中
            random_p.append(random.random())

        new_pop = []
        # 转轮盘选择法
        for i in range(len(random_p)):
            for j in range(len(new_fit_value)):
                if random_p[i] <= new_fit_value[j]:  # 看随机数落入了哪个区间
                    new_pop.append(self.pop[j])  # 将选中该的基因加入新种群
                    print(j + 1)
                    break

        return new_pop

    def sum(self, fit_value):
        """
        计算适应度之和
        :param fit_value: 种群适应度
        :return: 种群适应度之和
        """
        total = 0
        for v in fit_value:
            total += v
        return total

    def accum(self, fit_value):
        """
        计算累计概率
        :param fit_value: 百分比形式的种群适应度
        :return: 累计概率
        """
        for i in range(1, len(fit_value) - 1):
            fit_value[i] += fit_value[i - 1]  # 前i项的和赋值给fit_value[i]
            fit_value[-1] = 1  # 最后一项为1

    def crossover(self):
        pop_len = len(self.pop)
        for i in range(0, pop_len, 2):  # 这里为什么不随机选两个？
            r = random.random()  # 随机产生0~1的数
            if r < self.pc:  # 满足交叉的概率，进行交叉
                cpoint = random.randint(0, len(self.pop[0]))  # 随机产生交换位点
                temp1 = []
                temp2 = []

                # 利用extend方法和列表切片，组成新的两个基因
                temp1.extend(self.pop[i][0:cpoint])
                temp1.extend(self.pop[i + 1][cpoint:len(self.pop[i])])
                temp2.extend(self.pop[i + 1][0:cpoint])
                temp2.extend(self.pop[i][cpoint:len(self.pop[i])])
                # 交换形成的新基因返回种群
                self.pop[i] = temp1
                self.pop[i + 1] = temp2

    def mutation(self):
        px = len(self.pop)
        py = len(self.pop[0])

        for i in range(px):
            r = random.random()
            print(r)
            if r < pm:
                mpoint = random.randint(0, py - 1)  # 随机产生变异位点
                # 进行变异
                # 或者可以写成 pop[i][mpoint] = !pop[i][mpoint]
                if self.pop[i][mpoint] == 1:
                    self.pop[i][mpoint] = 0
                else:
                    self.pop[i][mpoint] = 1