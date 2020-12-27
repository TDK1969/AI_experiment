#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter as tk
import time
import random
import json
from functools import partial
from settings import COLUMN,ROW,DEPTH
import settings
import Minimax_Alphabeta
import evolution

ChessBoard = {}
DataBoard = []
LOG_LINE_NUM = 0
Algorithms = ['Minimax_Alpha-beta', 'Evolution', 'b']


class Board():
    def __init__(self, window):
        self.window = window
        self.player = True  # True is black, False is white
        self.Roboot_first = False
        self.Algo_v = tk.IntVar()
        self.used_time = 0
        self.steps = 0
        self.status = False
        self.column = COLUMN
        self.row = ROW
        self.map_pos = (2, 2)
        self.cell = [tk.PhotoImage(file='pics/cell.png')]
        for i in range(2):
            pic = tk.PhotoImage(file='pics/cell{}.png'.format(i))
            self.cell.append(pic)
        self.corners = []
        for i in range(4):
            corner_pic = tk.PhotoImage(file='pics/corner{}.png'.format(i))
            self.corners.append([corner_pic])
            for j in range(2):
                corner_pic = tk.PhotoImage(
                    file='pics/corner{}{}.png'.format(i, j))
                self.corners[i].append(corner_pic)
        self.edges = []
        for i in range(4):
            edge_pic = tk.PhotoImage(file='pics/edge{}.png'.format(i))
            self.edges.append([edge_pic])
            for j in range(2):
                edge_pic = tk.PhotoImage(file='pics/edge{}{}.png'.format(i, j))
                self.edges[i].append(edge_pic)

    # 设置窗口
    def set_init_window(self):
        self.window.title("五子棋")  # 窗口名
        self.window.geometry('900x600+10+10')
        self.window["bg"] = "Azure"
        self.window.attributes("-alpha", 0.95)  # 虚化，值越小虚化程度越高

        # 框架
        ctrl_frame = tk.Frame(self.window, bg="Azure")
        ctrl_frame.pack(side='right', padx=60)
        chessboard_frame = tk.Frame(self.window)
        chessboard_frame.pack(side='right')

        button_frame = tk.Frame(ctrl_frame, bg="Azure")
        button_frame.pack(side='top')
        msg_frame = tk.Frame(ctrl_frame, bg="Azure")
        msg_frame.pack(side='top')

        left_frame = tk.Frame(button_frame, bg="Azure")
        left_frame.pack(side='left', padx=20)
        right_frame = tk.Frame(button_frame, bg="Azure")
        right_frame.pack(side='left', padx=20)

        # 提示框
        self.msg_text = tk.Text(
            msg_frame, width=40, height=25)
        self.msg_text.pack()

        # 控制按钮
        self.player_button = tk.Button(
            right_frame, text="白子", bg="lightblue", width=10, command=self.choose)
        self.begin_button = tk.Button(
            right_frame, text="开始", bg="lightblue", width=10, command=self.begin)
        self.player_button.pack(pady=10)
        self.begin_button.pack(pady=10)

        # 算法选择按钮
        i = 0
        for algo in Algorithms:
            button = tk.Radiobutton(
                left_frame, text=algo, bg="lightblue", width=20, value=i)
            button['command'] = partial(self.choose_algorithm, i)
            button['variable'] = self.Algo_v

            button.pack(pady=10)
            i += 1
        self.choose_algorithm(0)
        self.set_chessboard(chessboard_frame)

    def choose_algorithm(self, alg_num):
        if self.status:
            return
        self.Algo_v.set(alg_num)
        if alg_num == 0:
            self.Algorithm = Minimax_Alphabeta.MAB()
        if alg_num == 1:
            self.Algorithm = evolution.evolution()

        self.write_to_Text("已选"+Algorithms[alg_num]+'算法')

    def choose(self):
        if self.status:
            return
        if not self.Roboot_first:
            self.write_to_Text("已选白子")
            self.player_button['text'] = "黑子"
        else:
            self.write_to_Text("已选黑子")
            self.player_button['text'] = "白子"
        self.Roboot_first = not self.Roboot_first

    # 判断棋子位置，给与button相应贴图
    def stick_image(self, i, j, button, pic):
        if i == 0 and j == 0:
            button['image'] = self.corners[0][pic]
        elif i == 0 and j == self.column-1:
            button['image'] = self.corners[1][pic]
        elif i == self.row-1 and j == self.column-1:
            button['image'] = self.corners[2][pic]
        elif i == self.row-1 and j == 0:
            button['image'] = self.corners[3][pic]
        elif i == 0:
            button['image'] = self.edges[0][pic]
        elif j == self.column-1:
            button['image'] = self.edges[1][pic]
        elif i == self.row-1:
            button['image'] = self.edges[2][pic]
        elif j == 0:
            button['image'] = self.edges[3][pic]
        else:
            button['image'] = self.cell[pic]

    # 布置棋盘
    def set_chessboard(self, chessboard_frame):
        cell_num = 0
        for i in range(self.row):
            DataBoard.append([])
            for j in range(self.column):
                new_cell = tk.Button(
                    chessboard_frame, bd=0, borderwidth=0, highlightthickness=0)
                self.stick_image(i, j, new_cell, 0)
                new_cell['command'] = partial(self.human_play, cell_num)
                new_cell.grid(row=i, column=j)
                ChessBoard[cell_num] = (True, (i, j), new_cell)
                DataBoard[i].append(0)
                cell_num += 1

    def check_win(self, i, j):
        dirs = [
            [(1, 0), (-1, 0)],
            [(0, 1), (0, -1)],
            [(1, 1), (-1, -1)],
            [(1, -1), (-1, 1)]
        ]
        for d in dirs:
            n = 0
            temi = i
            temj = j
            while temi >= 0 and temj >= 0 and temi < self.row and temj < self.column and DataBoard[i][j] == DataBoard[temi][temj]:
                temi += d[0][0]
                temj += d[0][1]
                n += 1
            temi = i + d[1][0]
            temj = j + d[1][1]
            while temi >= 0 and temj >= 0 and temi < self.row and temj < self.column and DataBoard[i][j] == DataBoard[temi][temj]:
                temi += d[1][0]
                temj += d[1][1]
                n += 1
            if n >= 5:
                return True
        return False

    # 放置棋子
    def put_chess(self, cell_num):
        cell = ChessBoard[cell_num]
        i, j = cell[1]
        print(cell[1])
        self.stick_image(i, j, cell[2], 1 + self.player)
        ChessBoard[cell_num] = (False, self.player, cell[1], cell[2])
        DataBoard[i][j] = 2 - self.player  # 黑1，白2
        if self.check_win(i, j):
            self.status = False
            if self.player:
                self.write_to_Text('黑方获胜')
            else:
                self.write_to_Text('白方获胜')
            self.write_to_Text('AI总用时%.2fs\t平均每步用时%.2fs' %
                               (self.used_time, self.used_time/self.steps))
            return
        else:
            self.player = not self.player

    def human_play(self, cell_num):
        if not self.status:
            self.write_to_Text("点击开始，开始游戏")
            return
        cell = ChessBoard[cell_num]
        if not cell[0]:  # 如果已经有棋子
            return
        self.put_chess(cell_num)
        self.roboot_play()

    def roboot_play(self):
        if not self.status:
            return
        i, j, time = self.Algorithm.GetBestPos(DataBoard, self.player)
        cell_num = i*self.column+j
        self.write_to_Text("AI用时%.2fs" % time)
        self.put_chess(cell_num)
        self.used_time += time
        self.steps += 1

    def begin(self):
        if self.status:
            self.write_to_Text("点击重玩，重开本局")
            return
        self.write_to_Text("游戏开始")
        self.status = True
        self.begin_button.configure(text="重玩", command=self.restart)
        if self.Roboot_first:
            self.roboot_play()

    def restart(self):
        self.player = True  # True is black, False is white
        self.Roboot_first = False
        self.status = False
        self.used_time = 0
        self.begin_button.configure(text="开始", command=self.begin)
        self.player_button['text'] = "白子"
        self.msg_text.delete(1.0, 'end')
        for i in range(self.row):
            for j in range(self.column):
                cell = ChessBoard[i*self.column+j]
                if not cell[0]:
                    self.stick_image(i, j, cell[3], 0)
                    ChessBoard[i*self.column+j] = (True, cell[2], cell[3])
                DataBoard[i][j] = 0
        pass

    # 获取当前时间
    def get_current_time(self):
        current_time = time.strftime(
            '%H:%M:%S', time.localtime(time.time()))
        return current_time

    # 日志动态打印
    def write_to_Text(self, msg):
        global LOG_LINE_NUM
        current_time = self.get_current_time()
        msg_in = str(current_time) + " " + str(msg) + "\n"  # 换行
        if LOG_LINE_NUM <= 25:
            self.msg_text.insert(tk.END, msg_in)
            LOG_LINE_NUM = LOG_LINE_NUM + 1
        else:
            self.msg_text.delete(1.0, 2.0)
            self.msg_text.insert(tk.END, msg_in)

def main():
    init_window = tk.Tk()
    GobangBoard = Board(init_window)
    GobangBoard.set_init_window()
    init_window.mainloop()

main()
