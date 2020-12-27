from settings import ROW, COLUMN, DEPTH
import random
import copy
import time
import sys
import threading
from evaluate import *

# 棋型 权重
OTHER = 0
ONE = 10
TWO = 100
THREE = 1000
FOUR = 100000
FIVE = 10000000
BLOCKED_TWO = 10
BLOCKED_THREE = 100
BLOCKED_FOUR = 10000

class MAB():
    def __init__(self):
        self.depth = DEPTH

    def GetBestPos(self, Databoard, player):
        """
        获取AI下的最好的位置
        :param Databoard: 棋盘，空为0，黑1，白2
        :param player: AI下的棋子，True-黑，False-白
        :return:
        """
        BeginTime = time.time()
        # 深拷贝一个棋盘
        self.Databoard = copy.deepcopy(Databoard)
        # 将墙壁位置赋值为-1
        self.Databoard.insert(0, [-1]*COLUMN)
        self.Databoard.append([-1]*COLUMN)
        for row in self.Databoard:
            row.insert(0, -1)
            row.append(-1)

        # 判断黑白子
        if player:
            self.ComRole = 1
            self.HumRole = 2
        else:
            self.ComRole = 2
            self.HumRole = 1

        Best = self.MinMax_AlphaBeta(self.depth)
        EndTime = time.time()
        UsedTime = EndTime - BeginTime
        return Best[0]-1, Best[1]-1, UsedTime

    def has_neighbor(self, x, y):
        """
        判断某位置周围是否有已经下的棋子，缩小搜索范围
        :param x: 位置的x坐标
        :param y: 位置的y坐标
        :return: 该位置周围是否有棋子
        """
        n = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                cur_x = x + i
                cur_y = y + j
                if cur_x < 1 or cur_y < 1 or cur_x > ROW or cur_y > COLUMN or (cur_x, cur_y) == (x, y):
                    continue
                n += self.Databoard[cur_x][cur_y]
        return n != 0

    def neighbor_cell(self):
        """
        遍历整个棋盘，返回周围有棋子的空位
        :return: 周围有棋子的空位
        """
        nodes = []
        for i in range(ROW+1):
            if i == 0:
                continue
            for j in range(COLUMN+1):
                if self.Databoard[i][j] != 0:
                    continue
                if self.has_neighbor(i, j):
                    nodes.append((i, j))
        return nodes

    def ScoreTable(self, Number, Empty):
        if Number >= 5:
            return FIVE
        elif Number == 4:
            if Empty == 2:
                return FOUR
            elif Empty == 1:
                return BLOCKED_FOUR
        elif Number == 3:
            if Empty == 2:
                return THREE
            elif Empty == 1:
                return BLOCKED_THREE
        elif Number == 2:
            if Empty == 2:
                return TWO
            elif Empty == 1:
                return BLOCKED_TWO
        elif Number == 1 and Empty == 2:
                return ONE
        return OTHER
    
    def CountScore(self, Chesses, Role): # 正斜线、反斜线、横、竖，均转成一维数组来计算
        """
        计算分数
        :param Chesses:
        :param Role:
        :return:
        """
        Scoretmp = 0
        Empty = 0
        Number = 0
        
        for c in Chesses:
            if c == Role:
                Number += 1
            elif c == 0:
                if Number == 0:
                    Empty = 1
                else:
                    Scoretmp += self.ScoreTable(Number, Empty + 1)
                    Empty = 1
                    Number = 0
            else:
                Scoretmp += self.ScoreTable(Number, Empty)
                Empty = 0
                Number = 0
        Scoretmp += self.ScoreTable(Number, Empty)
        return Scoretmp

    def TDK_evaluate(self, x, y, player, enemy):
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
        value = TDK_value(enemy, player, list1, list2, list3, list4)

        return value
        

    def Evaluate(self): # 评估函数，评估局势
        ScoreCom = 0
        ScoreHum = 0
        # 横排
        for i in range(1, ROW+1):
            Chesses = self.Databoard[i]
            ScoreCom += self.CountScore(Chesses, self.ComRole)
            ScoreHum += self.CountScore(Chesses, self.HumRole)

        # 竖排
        Chesses = []
        for j in range(1, COLUMN+1):
            for i in range(1, ROW+1):
                Chesses.append(self.Databoard[i][j])
            ScoreCom += self.CountScore(Chesses, self.ComRole)
            ScoreHum += self.CountScore(Chesses, self.HumRole)
            Chesses.clear()

        # 正斜线
        for i in range(1-COLUMN, COLUMN):
            for x in range(1, COLUMN+1):
                y = x - i
                if x > 0 and y > 0 and x <= COLUMN and y <=ROW:
                    Chesses.append(self.Databoard[x][y])
            ScoreCom += self.CountScore(Chesses, self.ComRole)
            ScoreHum += self.CountScore(Chesses, self.HumRole)
            Chesses.clear()

        # 反斜线
        for i in range(2, 2*COLUMN+1):
            for x in range(1, COLUMN+1):
                y = - x + i
                if x > 0 and y > 0 and x <= COLUMN and y <=ROW:
                    Chesses.append(self.Databoard[x][y])
            ScoreCom += self.CountScore(Chesses, self.ComRole)
            ScoreHum += self.CountScore(Chesses, self.HumRole)
            Chesses.clear()

        # 返回电脑的分数与玩家的分数之差
        return ScoreCom - ScoreHum

    def Evaluate1(self, x, y):  # 评估函数，评估局势
        ScoreCom = 0
        ScoreHum = 0
        # 横排

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

        ScoreCom += self.CountScore(list1, self.ComRole) + self.CountScore(list2, self.ComRole) + \
                    self.CountScore(list3, self.ComRole) + self.CountScore(list4, self.ComRole)
        ScoreHum += self.CountScore(list1, self.HumRole) + self.CountScore(list2, self.HumRole) + \
                    self.CountScore(list3, self.HumRole) + self.CountScore(list4, self.HumRole)
        # 返回电脑的分数与玩家的分数之差
        return ScoreCom - ScoreHum


    def Min_AlphaBeta(self, depth, alpha, beta, x, y):
        # 极小层，搜索人类下的位置，求极小的评分
        # 如果到达最后一层，返回当前棋局评分即可
        score = self.TDK_evaluate(x, y, self.HumRole, self.ComRole)
        BestScore = 0
        """
        if depth == 0:
            #score = self.Evaluate1(x, y)
            score = self.TDK_evaluate(x, y, self.HumRole, self.ComRole)
            return score
        """
        if depth != 0:

            nodes = self.neighbor_cell()

            # 遍历所有可走位置
            # MIN层，寻找最小的评分。在已经寻找的孩子节点中，BestScore目前为止找到的最小
            # 若ChildScore < BestScore，则更新BestScore，并将这层alpha和BestScore中的较小值传入下一层的alpha，比alpha的大的分支则减去
            BestScore = sys.maxsize
            for n in nodes:
                self.Databoard[n[0]][n[1]] = self.HumRole  # 假设在这个位置落子
                ChildScore = self.Max_AlphaBeta(depth-1, min(BestScore, alpha), beta, n[0], n[1])
                self.Databoard[n[0]][n[1]] = 0  # 复原
                if ChildScore < BestScore:
                    BestScore = ChildScore
                # beta是上一层传入的最大值，上一层是MAX层，寻找的是最大值
                # 这一层是MIN层，找最小值，如果此时评分已经比beta小了就不用再往下遍历了
                # 因为返回值一定比现在的评分更小，上一层找最大值，一定不会被采用
                if ChildScore <= beta:
                    break
        return score + BestScore


    def Max_AlphaBeta(self, depth, alpha, beta, x, y):
        # 如果到达最后一层，返回当前棋局评分即可
        score = self.TDK_evaluate(x, y, self.ComRole, self.HumRole)
        BestScore = 0
        """
        if depth == 0:
            #score = self.Evaluate1(x, y)
            score = self.TDK_evaluate(x, y, self.ComRole, self.HumRole)
            return score
        """
        if depth != 0:
            nodes = self.neighbor_cell()

            # 遍历所有可走位置
            # MAX层，寻找最大的评分。在已经寻找的孩子节点中，BestScore目前为止找到的最大
            # 若ChildScore > BestScore，则更新BestScore，并将这层beta和BestScore中的较大值传入下一层的beta，比beta的小的分支则减去
            BestScore = -sys.maxsize
            for n in nodes:
                self.Databoard[n[0]][n[1]] = self.ComRole
                ChildScore = self.Min_AlphaBeta(depth-1, alpha, max(BestScore, beta), n[0], n[1])
                self.Databoard[n[0]][n[1]] = 0
                if ChildScore > BestScore:
                    BestScore = ChildScore
                # alpha是上一层传入的最小值，上一层是MIN层，寻找的是最小值
                # 这一层是MAX层，找最大值，如果此时评分已经比alpha大了就不用再往下遍历了
                # 因为返回值一定比现在的评分更大，上一层找最小值，一定不会被采用
                if ChildScore >= alpha:
                    break
        return score + BestScore
    
    def MinMax_AlphaBeta(self, depth):
        nodes = self.neighbor_cell()
        BestScore = -sys.maxsize
        ChildNode = []
        for n in nodes:
            self.Databoard[n[0]][n[1]] = self.ComRole
            ChildScore = self.Min_AlphaBeta(depth - 1, sys.maxsize, -sys.maxsize, n[0], n[1])
            if ChildScore > BestScore:
                BestScore = ChildScore
                ChildNode.clear()  # 如果出现新的最大值则清空ChildNode列表
            if ChildScore == BestScore:  # 将最优下法加入
                ChildNode.append(n)
            self.Databoard[n[0]][n[1]] = 0
        # 随机选择一个节点返回
        return random.choice(ChildNode)