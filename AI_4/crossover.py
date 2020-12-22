# 0.0 coding:utf-8 0.0
# 交配

import random


def crossover(pop, pc):
    pop_len = len(pop)
    for i in range(0, pop_len, 2):
        r = random.random()
        print(r)
        if(r < pc):
            cpoint = random.randint(0,len(pop[0]))
            temp1 = []
            temp2 = []

            temp1.extend(pop[i][0:cpoint])
            temp1.extend(pop[i+1][cpoint:len(pop[i])])
            temp2.extend(pop[i+1][0:cpoint])
            temp2.extend(pop[i][cpoint:len(pop[i])])
            pop[i] = temp1
            pop[i+1] = temp2