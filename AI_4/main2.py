import numpy as np
import random as rd
import matplotlib.pyplot as plt
from F import F

# 蚂蚁数量
Ant = 300
# 移动次数
Times = 80
# 信息素发挥系数
Rou = 0.9
# 转移概率
P0 = 0.2
# 搜索范围
Lower_1 = -1
Upper_1 = 1
Lower_2 = -1
Upper_2 = 1

X = np.zeros((Ant, 2), dtype=np.float64)
Tau = np.zeros(Ant, dtype=np.float64)
# 初始化蚂蚁的坐标
for i in range(Ant):
    X[i][0] = (Lower_1+(Upper_1-Lower_1)*rd.random())
    X[i][1] = (Lower_1+(Upper_2-Lower_2)*rd.random())
    # 信息素
    Tau[i] = F(X[i][0], X[i][1])

step = 0.05
x = np.arange(Lower_1, Upper_1, step)
y = np.arange(Lower_2, Upper_2, step)
x, y = np.meshgrid(x, y)
z = F(x, y)

fig = plt.figure(figsize=plt.figaspect(0.5))
ax = fig.add_subplot(1, 2, 1, projection='3d')
surf = ax.plot_surface(x, y, z, rstride=1, cstride=1, cmap='winter', alpha=.5)

ax.scatter(X[:, 0], X[:, 1], F(X[:, 0], X[:, 1]), c='k', marker='*')
ax.set_xlabel('$X$')
ax.set_ylabel('$Y$')
ax.set_zlabel(r'$f(x,y)$')
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
ax.set_title("蚂蚁的初始位置分布")

Tau_Best = np.zeros(Times, dtype=np.float64)

for t in range(Times):
    lamda = 1.0/(t+1)
    BestIndex = np.argmax(Tau)
    Tau_Best[t] = np.max(Tau)
    P = np.zeros((Times, Ant), dtype=np.float64)
    for a in range(Ant):
        P[t][a] = (Tau[BestIndex]-Tau[a])/Tau[BestIndex]
    for a in range(Ant):
        if P[t][a] < P0:  # 局部搜索
            temp1 = X[a][0]+(2*rd.random()-1)*lamda
            temp2 = X[a][1]+(2*rd.random()-1)*lamda
        else:  # 全局搜索
            temp1 = X[a][0]+(Upper_1-Lower_1)*(rd.random()-0.5)
            temp2 = X[a][1]+(Upper_2-Lower_2)*(rd.random()-0.5)
        # 越界处理
        if temp1 < Lower_1:
            temp1 = Lower_1
        if temp1 > Upper_1:
            temp1 = Upper_1
        if temp2 < Lower_2:
            temp2 = Lower_2
        if temp2 > Upper_2:
            temp2 = Upper_2
        # 是否更新位置
        if F(temp1, temp2) > F(X[a][0], X[a][1]):
            X[a][0] = temp1
            X[a][1] = temp2
    # 更新信息素
    for a in range(Ant):
        Tau[a] = (1-Rou)*Tau[a]+F(X[a][0], X[a][1])

ax = fig.add_subplot(1, 2, 2, projection='3d')
surf = ax.plot_surface(x, y, z, rstride=1, cstride=1, cmap='winter', alpha=.5)
ax.scatter(X[:, 0], X[:, 1], F(X[:, 0], X[:, 1]), c='k', marker='*')
ax.set_title("蚂蚁的最终位置分布")
ax.set_xlabel('$X$')
ax.set_ylabel('$Y$')
ax.set_zlabel(r'$f(x,y)$')
plt.show()
