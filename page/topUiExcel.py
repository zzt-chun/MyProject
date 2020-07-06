# -*- coding: utf-8 -*-
# @Time    : 2019/11/25 17:14
# @Author  : zzt
# @File    : topUiExcel.py
import tkinter as tk
from tkinter import ttk


class TopUiExcel():
    '''
    生成一个顶级窗口显示两个excel内容
    '''

    def __init__(self, name, data1, data2):
        self.root = tk.Toplevel()
        self.root.title(name)
        self.create_excel(data1, data2)

    def fun_left(self, event):
        idd = self.tree.identify_row(event.y)  # 获取表一点击选中行数
        self.tree_1.selection_set(idd)  # 设置表二中与表一相同位置为选中状态
        x, y = self.tree.yview()  # 获取表一滚动条位置
        self.tree_1.yview(tk.MOVETO, x)  # 设置表二滚动条位置与表一一致
        x_x, x_y = self.tree.xview()
        self.tree_1.xview(tk.MOVETO, x_x)
        '''
        print('x, y = ', event.x, event.y)
        print('idd, col = ', self.tree.identify_row(event.y), self.tree.identify_column(event.x))
        print('bbox= ', self.tree.bbox(self.tree.identify_row(event.y), self.tree.identify_column(event.x)))
        '''

    def fun_right(self, event):
        idd = self.tree_1.identify_row(event.y)  # 获取表一点击选中行数
        self.tree.selection_set(idd)  # 设置表二中与表一相同位置为选中状态
        x, y = self.tree_1.yview()  # 获取表一滚动条位置
        self.tree.yview(tk.MOVETO, x)  # 设置表二滚动条位置与表一一致
        x_x, x_y = self.tree_1.xview()
        self.tree.xview(tk.MOVETO, x_x)

    def create_excel(self, data1, data2):
        self.root.resizable(0, 0)
        f1 = tk.Frame(self.root)
        f2 = tk.Frame(self.root)
        f3 = tk.Frame(f1, width=800, height=600)
        f4 = tk.Frame(f2, width=800, height=600)
        f3.pack_propagate(0)  # 使width=800, height=600有效
        f4.pack_propagate(0)
        f3.pack(side=tk.LEFT)
        f4.pack(side=tk.LEFT)
        f1.grid(row=0, column=0)
        f2.grid(row=0, column=1)
        sb1 = tk.Scrollbar(f3, orient=tk.HORIZONTAL)  # 横向拉条
        sb1.pack(side=tk.BOTTOM, fill=tk.BOTH)
        sb3 = tk.Scrollbar(f1, orient=tk.VERTICAL)  # 竖向拉条
        sb3.pack(side=tk.RIGHT, fill=tk.BOTH)
        sb2 = tk.Scrollbar(f4, orient=tk.HORIZONTAL)  # 横向拉条
        sb2.pack(side=tk.BOTTOM, fill=tk.BOTH)
        sb4 = tk.Scrollbar(f4, orient=tk.VERTICAL)  # 竖向拉条
        sb4.pack(side=tk.RIGHT, fill=tk.BOTH)

        self.tree = ttk.Treeview(f3, show='headings', xscrollcommand=sb1.set, yscrollcommand=sb3.set)  # 表格
        self.tree_1 = ttk.Treeview(f4, show='headings', xscrollcommand=sb2.set, yscrollcommand=sb4.set)  # 表格
        self.tree.pack(side=tk.TOP, expand="yes", fill="both")
        self.tree_1.pack(side=tk.TOP, expand="yes", fill="both")
        sb1.config(command=self.tree.xview)
        sb2.config(command=self.tree_1.xview)
        sb3.config(command=self.tree.yview)
        sb4.config(command=self.tree_1.yview)
        self.tree.bind('<Button-1>', self.fun_left)
        self.tree_1.bind('<Button-1>', self.fun_right)
        # 读取excel内容

        self.tree['height'] = 28  # 设置展示的行数
        self.tree_1['height'] = 28  # 设置展示的行数

        self.tree["columns"] = data1[0]
        self.tree_1["columns"] = data2[0]

        if len(data1[0]) != len(data2[0]):
            print("两个表头列名个数不相同 data1=%s, data2=%s" % (data1[0], data2[0]))

        for name in data1[0]:
            self.tree.column(name, width=10 * 8)  # 设置宽度
            self.tree.heading(name, text=name)  # 显示表头

        for name in data2[0]:
            self.tree_1.column(name, width=10 * 8)  # 设置宽度
            self.tree_1.heading(name, text=name)  # 显示表头

        key = 0
        # self.tree.tag_configure('ttk', background='yellow')
        for row in data1:
            if key != 0:
                # if key in list(range(1, 20, 2)):
                #     self.tree.insert('', str(key), values=row, tags='ttk')  # 染色
                # else:
                #     self.tree.insert('', str(key), values=row)  # 插入数据
                self.tree.insert('', str(key), values=row)  # 插入数据
            key += 1
        key = 0
        for row in data2:
            if key != 0:
                self.tree_1.insert('', str(key), values=row)  # 插入数据
            key += 1


class GitTopUiInfo(object):
    '''
    生成一个顶级窗口显示两个git提交信息
    '''

    def __init__(self, name, data1, data2):
        self.root = tk.Toplevel()
        self.root.title(name)
        self.create_excel(data1, data2)

    def fun_left(self, event):
        idd = self.tree.identify_row(event.y)  # 获取表一点击选中行数
        # print("idd = %s" % str(idd))
        # self.tree_1.selection_set(idd)  # 设置表二中与表一相同位置为选中状态
        # x, y = self.tree.yview()  # 获取表一滚动条位置
        # self.tree_1.yview(tk.MOVETO, x)  # 设置表二滚动条位置与表一一致
        # x_x, x_y = self.tree.xview()
        # self.tree_1.xview(tk.MOVETO, x_x)
        # print("x1, y1 = %s,  %s" % (x, y))
        # print("x2, y2 = %s,  %s" % (x_x, x_y))
        '''
        print('x, y = ', event.x, event.y)
        print('idd, col = ', self.tree.identify_row(event.y), self.tree.identify_column(event.x))
        print('bbox= ', self.tree.bbox(self.tree.identify_row(event.y), self.tree.identify_column(event.x)))
        '''
        print("type(idd) = %s, idd = %s" % (type(idd), idd))
        vals = self.tree.item(idd, "values")
        _num = int(vals[-1])
        if _num <= 0:
            return
        elif 0 < _num < 16:
            num = "I00" + hex(_num)[2:].upper()
        elif 16 <= _num < 256:
            num = "I0" + hex(_num)[2:].upper()
        else:
            num = "I" + hex(_num)[2:].upper()
            # print("num = %s" % str(_num))
            # print("目标id:", num)
        self.tree_1.selection_set(num)  # 设置表二中与表一相同位置为选中状态
        self.tree_1.see(num)

    def fun_right(self, event):
        idd = self.tree_1.identify_row(event.y)  # 获取表一点击选中行数
        print("type(idd) = %s, idd = %s" % (type(idd), idd))
        vals = self.tree_1.item(idd, "values")
        # print("选中的为： %s" % str(vals))
        _num = int(vals[-1])
        if _num <= 0:
            return
        elif 0 < _num < 16:
            num = "I00" + hex(_num)[2:].upper()
        elif 16 <= _num < 256:
            num = "I0" + hex(_num)[2:].upper()
        else:
            num = "I" + hex(_num)[2:].upper()

        self.tree.selection_set(num)  # 设置表二中与表一相同位置为选中状态
        # x, y = self.tree_1.yview()  # 获取表一滚动条位置
        # self.tree.yview(tk.MOVETO, x)  # 设置表二滚动条位置与表一一致
        # x_x, x_y = self.tree_1.xview()
        # self.tree.xview(tk.MOVETO, x_x)
        # self.tree.see(vals[-1])
        # print("num = %s" % str(_num))
        # print("目标id:", num)
        self.tree.see(num)
        # print("x1, y1 = %s,  %s" % (x, y))
        # print("x2, y2 = %s,  %s" % (x_x, x_y))
        # self.tree.yview_moveto(1.0)    #定位到最后一行

    def create_excel(self, data1, data2):
        self.root.resizable(0, 0)
        f1 = tk.Frame(self.root)
        f2 = tk.Frame(self.root)
        f3 = tk.Frame(f1, width=900, height=600)
        f4 = tk.Frame(f2, width=900, height=600)
        f3.pack_propagate(0)  # 使width=900, height=600有效
        f4.pack_propagate(0)
        f3.pack(side=tk.LEFT)
        f4.pack(side=tk.LEFT)
        f1.grid(row=0, column=0)
        f2.grid(row=0, column=1)
        sb1 = tk.Scrollbar(f3, orient=tk.HORIZONTAL)  # 横向拉条
        sb1.pack(side=tk.BOTTOM, fill=tk.BOTH)
        sb3 = tk.Scrollbar(f1, orient=tk.VERTICAL)  # 竖向拉条
        sb3.pack(side=tk.RIGHT, fill=tk.BOTH)
        sb2 = tk.Scrollbar(f4, orient=tk.HORIZONTAL)  # 横向拉条
        sb2.pack(side=tk.BOTTOM, fill=tk.BOTH)
        sb4 = tk.Scrollbar(f4, orient=tk.VERTICAL)  # 竖向拉条
        sb4.pack(side=tk.RIGHT, fill=tk.BOTH)

        self.tree = ttk.Treeview(f3, show='headings', xscrollcommand=sb1.set, yscrollcommand=sb3.set,
                                 columns=list(data1[0].keys()))  # 表格
        self.tree_1 = ttk.Treeview(f4, show='headings', xscrollcommand=sb2.set, yscrollcommand=sb4.set,
                                   columns=list(data1[0].keys()))  # 表格
        self.tree.pack(side=tk.TOP, expand="yes", fill="both")
        self.tree_1.pack(side=tk.TOP, expand="yes", fill="both")
        sb1.config(command=self.tree.xview)
        sb2.config(command=self.tree_1.xview)
        sb3.config(command=self.tree.yview)
        sb4.config(command=self.tree_1.yview)
        self.tree.bind('<Button-1>', self.fun_left)
        self.tree_1.bind('<Button-1>', self.fun_right)
        # 读取excel内容

        self.tree['height'] = 28  # 设置展示的行数
        self.tree_1['height'] = 28  # 设置展示的行数

        self.tree["columns"] = list(data1[0].keys())
        self.tree_1["columns"] = list(data2[0].keys())

        if len(data1[0].keys()) != len(data2[0].keys()):
            print("两个表头列名个数不相同 data1=%s, data2=%s" % (data1[0], data2[0]))

        for key, value in data1[0].items():
            self.tree.column(key, width=value)  # 设置宽度
            self.tree.heading(key, text=key)  # 显示表头

        for key, value in data2[0].items():
            self.tree_1.column(key, width=value)  # 设置宽度
            self.tree_1.heading(key, text=key)  # 显示表头

        key = 0
        self.tree.tag_configure("yel", background='Chartreuse')
        self.tree.tag_configure("gray", background='Gray')
        self.tree.tag_configure("red", background='red')
        self.tree_1.tag_configure("yel", background='Chartreuse')
        self.tree_1.tag_configure("red", background='red')
        self.tree_1.tag_configure("gray", background='Gray')
        colour = {1: "yel", 2: "red", 0: "", 3: "gray"}
        for row in data1:
            if key != 0:
                # if key in list(range(1, 20, 2)):
                #     self.tree.insert('', str(key), values=row, tags='ttk')  # 染色
                # else:
                #     self.tree.insert('', str(key), values=row)  # 插入数据
                self.tree.insert('', str(key), values=row, tags=colour[row[-2]])  # 插入数据
            key += 1
        key = 0
        for row in data2:
            if key != 0:
                # self.tree_1.insert('', str(key), values=row)  # 插入数据
                self.tree_1.insert('', str(key), values=row, tags=colour[row[-2]])  # 插入数据
            key += 1
