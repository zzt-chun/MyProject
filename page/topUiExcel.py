# -*- coding: utf-8 -*-
# @Time    : 2019/11/25 17:14
# @Author  : zzt
# @File    : topUiExcel.py
import tkinter as tk
from tkinter import ttk
import datetime
from tkinter import filedialog
from tkinter import messagebox
from Util import dataanalyze
import os
import json

class TopUiExcel(object):
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


class TopUiDeepExcel(object):
    '''
    生成一个顶级窗口显示两个excel内容
    tableName 表名
    data1
    data2
    '''

    relation = ['>', '=', '<', '>=', '<=', "包含", '不包含']
    definition = ["一列", "二列", "三列", "key", "rule", "value", "table_key"]

    def __init__(self, tableName, data1, data2, table_key, names, comand):
        self.root = tk.Toplevel()
        self.root.title(tableName)
        self.tableName = tableName
        self.names = names[1]
        self.saveKeyPath = ''
        self.isReset = True
        self.create_excel(data1, data2)
        self.resetRules(table_key)
        self.command = comand

    def resetRules(self, data=None):
        if not data:
            self.rules = {
                self.definition[0]: {self.definition[3]: '', self.definition[4]: '', self.definition[5]: ''},
                self.definition[1]: {self.definition[3]: '', self.definition[4]: '', self.definition[5]: ''},
                self.definition[2]: {self.definition[3]: '', self.definition[4]: '', self.definition[5]: ''},
                self.definition[6]: '',

            }
            self.isReset = True
        else:
            self.isReset = False
            self.rules = data

        self.resetButton()
        self.insert_info("初始化成功", 1, 1)

    def resetButton(self):
        if self.rules[self.definition[0]][self.definition[3]] != '':
            self.com1.set(self.rules[self.definition[0]][self.definition[3]])
        else:
            self.com1.set('筛选条件')

        if self.rules[self.definition[0]][self.definition[4]] != "":
            self.com2.set(self.rules[self.definition[0]][self.definition[4]])
        else:
            self.com2.set('=')

        if self.rules[self.definition[1]][self.definition[3]] != '':
            self.com1_1.set(self.rules[self.definition[1]][self.definition[3]])
        else:
            self.com1_1.set('筛选条件')

        if self.rules[self.definition[1]][self.definition[4]] != "":
            self.com2_1.set(self.rules[self.definition[1]][self.definition[4]])
        else:
            self.com2_1.set('=')

        if self.rules[self.definition[1]][self.definition[5]] != '':
            self.ent1_v_1.set(self.rules[self.definition[1]][self.definition[5]])
        else:
            self.ent1_v_1.set("")

        if self.rules[self.definition[1]][self.definition[3]] != '':
            self.com1_2.set(self.rules[self.definition[2]][self.definition[3]])
        else:
            self.com1_2.set('筛选条件')

        if self.rules[self.definition[2]][self.definition[4]] != "":
            self.com2_2.set(self.rules[self.definition[2]][self.definition[4]])
        else:
            self.com2_2.set('=')

        if self.rules[self.definition[2]][self.definition[5]] != '':
            self.ent1_v_2.set(self.rules[self.definition[2]][self.definition[5]])
        else:
            self.ent1_v_2.set("")

        if self.rules[self.definition[0]][self.definition[5]] != '':
            self.ent1_v.set(self.rules[self.definition[0]][self.definition[5]])
        else:
            self.ent1_v.set("")

        if self.rules[self.definition[6]] != '':
            self.com1_3.set(self.rules[self.definition[6]])
        else:
            self.com1_3.set("筛选条件")


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

    def insert_info(self, information, use_time=0, tag=0):
        if use_time:
            time = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S') + ': '
        else:
            time = ''
        this_tag = ''
        if tag == 1:
            this_tag = 'tag1'
        elif tag == 2:
            this_tag = 'tag2'
        self.tex.insert(tk.END, time + information + '\n', this_tag)

    def choose_key(self, com, index, key):
        if index == 0:
            self.rules[key] = com.get()
            self.insert_info('<%s>选择成功： %s' % (key, self.rules[key]), 1)
        else:
            self.rules[index][key] = com.get()
            self.insert_info('<%s>选择<%s>成功： %s' % (index, key, self.rules[index][key]), 1)
        if self.isReset:
            self.isReset = False

    def saveKeyRule2excel(self):
        if self.saveKeyPath == '':
            self.insert_info("没有选择路径", 1, 2)
            return

        if not os.path.exists(self.saveKeyPath):
            self.insert_info("目标路径不存在： %s" % self.saveKeyPath)
            return

        # if self.isReset:
        #     self.insert_info("请先设置筛选条件", 1, 2)
        #     return

        # snap_rules =
        self.rules[self.definition[2]][self.definition[5]] = self.ent1_v_2.get()
        self.rules[self.definition[0]][self.definition[5]] = self.ent1_v.get()
        self.rules[self.definition[1]][self.definition[5]] = self.ent1_v_1.get()
        if self.rules[self.definition[2]][self.definition[5]] != "":
            self.rules[self.definition[2]][self.definition[4]] = self.com2_2.get()
        if self.rules[self.definition[1]][self.definition[5]] != "":
            self.rules[self.definition[1]][self.definition[4]] = self.com2_1.get()
        if self.rules[self.definition[0]][self.definition[5]] != "":
            self.rules[self.definition[0]][self.definition[4]] = self.com2.get()
        try:
            result = dataanalyze.modifyExcel(self.saveKeyPath, [self.tableName, self.rules])
        except Exception as e:
            self.insert_info(str(e), 1, 2)
            return
        if not result[0]:
            self.insert_info(result[1], 1, 2)
        else:
            self.insert_info("保存成功： %s" % self.saveKeyPath, 1, 1)



    def import_file(self, v):
        path = filedialog.askopenfilename(filetypes=[('XLSX', '.xlsx'), ('XLS', '.xls')])
        if path == '':
            self.insert_info("没有选中导入文件", 1, 1)
            return
        v.set(path)
        self.saveKeyPath = path
        self.insert_info("选择路径成功： %s" % path, 1, 1)

    def deepDiff(self):
        self.rules[self.definition[2]][self.definition[5]] = self.ent1_v_2.get()
        self.rules[self.definition[0]][self.definition[5]] = self.ent1_v.get()
        self.rules[self.definition[1]][self.definition[5]] = self.ent1_v_1.get()
        if self.rules[self.definition[2]][self.definition[5]] != "":
            self.rules[self.definition[2]][self.definition[4]] = self.com2_2.get()
        if self.rules[self.definition[1]][self.definition[5]] != "":
            self.rules[self.definition[1]][self.definition[4]] = self.com2_1.get()
        if self.rules[self.definition[0]][self.definition[5]] != "":
            self.rules[self.definition[0]][self.definition[4]] = self.com2.get()
        # deep_diff中False弃用
        data1, data2 = self.command.deep_diff(self.rules, False)
        self.deleteAllTree()
        self.insert_info_for_tree(data1, data2)
        self.insert_info("重新比对完成", 1, 1)

    def deleteAllTree(self):

        [self.tree.delete(item) for item in self.tree.get_children()]
        [self.tree_1.delete(item) for item in self.tree_1.get_children()]


    def create_excel(self, data1, data2):
        self.root.resizable(0, 0)
        # ------------------ 功能区 ------------------
        labelf = tk.LabelFrame(self.root, text='功能区：')
        labelf.pack(anchor=tk.N, expand=True)

        # ------------------ 搜索条件 ------------------
        labelf_2 = tk.LabelFrame(labelf, text='搜索条件（可选）：')
        labelf_2.grid(row=0, column=0, padx=20, pady=5)
        self.com1 = ttk.Combobox(labelf_2, state='readonly', width=10)
        self.com1.bind("<<ComboboxSelected>>", lambda *args: self.choose_key(self.com1, self.definition[0], self.definition[3]))

        self.com1['values'] = self.names
        self.com1.grid(row=0, column=0, padx=10, pady=3)
        # 添加选择数据库下拉按钮
        self.com2 = ttk.Combobox(labelf_2, state='readonly', width=3)
        self.com2.bind("<<ComboboxSelected>>", lambda *args: self.choose_key(self.com2, self.definition[0], self.definition[4]))
        self.com2['values'] = self.relation
        self.com2.grid(row=0, column=1, padx=3, pady=3)
        # 添加文本显示框
        self.ent1_v = tk.StringVar()
        ent1 = tk.Entry(labelf_2, textvariable=self.ent1_v, width=12)
        ent1.grid(row=0, column=2, padx=8, pady=1)

        self.com1_1 = ttk.Combobox(labelf_2, state='readonly', width=10)
        self.com1_1.bind("<<ComboboxSelected>>", lambda *args: self.choose_key(self.com1_1, self.definition[1], self.definition[3]))
        self.com1_1['values'] = self.names
        self.com1_1.grid(row=1, column=0, padx=10, pady=3)
        # 添加选择数据库下拉按钮
        self.com2_1 = ttk.Combobox(labelf_2, state='readonly', width=3)
        self.com2_1.bind("<<ComboboxSelected>>", lambda *args: self.choose_key(self.com2_1, self.definition[1], self.definition[4]))
        self.com2_1['values'] = self.relation
        self.com2_1.grid(row=1, column=1, padx=3, pady=3)
        # 添加文本显示框
        self.ent1_v_1 = tk.StringVar()
        ent1_1 = tk.Entry(labelf_2, textvariable=self.ent1_v_1, width=12)
        ent1_1.grid(row=1, column=2, padx=8, pady=1)

        self.com1_2 = ttk.Combobox(labelf_2, state='readonly', width=10)
        self.com1_2.bind("<<ComboboxSelected>>", lambda *args: self.choose_key(self.com1_2, self.definition[2], self.definition[3]))
        self.com1_2['values'] = self.names
        self.com1_2.grid(row=2, column=0, padx=10, pady=3)
        # 添加选择数据库下拉按钮
        self.com2_2 = ttk.Combobox(labelf_2, state='readonly', width=3)
        self.com2_2.bind("<<ComboboxSelected>>", lambda *args: self.choose_key(self.com2_2, self.definition[2], self.definition[4]))
        self.com2_2['values'] = self.relation
        self.com2_2.grid(row=2, column=1, padx=3, pady=3)
        # 添加文本显示框
        self.ent1_v_2 = tk.StringVar()
        ent1_2 = tk.Entry(labelf_2, textvariable=self.ent1_v_2, width=12)
        ent1_2.grid(row=2, column=2, padx=8, pady=1)

        # ------------------ 功能 ------------------
        labelf_3 = tk.LabelFrame(labelf, text='功能：')
        # labelf_3.pack(anchor=tk.S, expand=True)
        labelf_3.grid(row=0, column=1, padx=20, pady=1)
        tk.Label(labelf_3, text='选择基准key： ').grid(row=0, column=0, padx=5, pady=1, columnspan=2)
        self.com1_3 = ttk.Combobox(labelf_3, state='readonly', width=18)
        self.com1_3.bind("<<ComboboxSelected>>", lambda *args: self.choose_key(self.com1_3, 0, self.definition[6]))
        self.com1_3.set('筛选条件')
        self.com1_3['values'] = self.names
        self.com1_3.grid(row=0, column=2, padx=5, pady=3)
        tk.Button(labelf_3, text='深度比对', width=18, command=lambda: self.deepDiff()).grid(row=1, column=0, padx=5, pady=5, columnspan=2)
        tk.Button(labelf_3, text='重置条件', width=16, command=lambda: self.resetRules()).grid(row=1, column=2, padx=5, pady=5)
        ent1_v_3 = tk.StringVar()
        ent1 = tk.Entry(labelf_3, textvariable=ent1_v_3, width=12)
        ent1_v_3.set('选择保存路径')
        ent1.grid(row=2, column=0, padx=3, pady=1)
        but2_1_1 = tk.Button(labelf_3, text='选择', command=lambda: self.import_file(ent1_v_3))
        but2_1_1.grid(row=2, column=1, padx=3, pady=1)
        tk.Button(labelf_3, text="保存筛选规则", width=16, command=lambda: self.saveKeyRule2excel()).grid(row=2, column=2, padx=5, pady=5)

        # ------------------ 日志 ------------------
        # 添加日志文本
        labelf_4 = tk.LabelFrame(labelf, text='日志文本：')
        # labelf_4.pack(anchor=tk.N, expand=True)
        labelf_4.grid(row=0, column=2, padx=20, pady=1)
        sb = tk.Scrollbar(labelf_4)
        sb.pack(side=tk.RIGHT, fill=tk.Y)
        # tex = tk.Text(labelf, height=33, yscrollcommand=sb.set, width=107)
        self.tex = tk.Text(labelf_4, height=10, yscrollcommand=sb.set, width=107)
        self.tex.tag_config('tag1', foreground='green')
        self.tex.tag_config('tag2', foreground='red')
        self.tex.pack(side=tk.LEFT, fill=tk.BOTH)
        sb.config(command=self.tex.yview)


        # 下半区部分UI
        # ------------------ 对比内容 ------------------
        labelf_1 = tk.LabelFrame(self.root, text='对比内容：')
        labelf_1.pack(anchor=tk.S, expand=True)

        f1 = tk.Frame(labelf_1)
        f2 = tk.Frame(labelf_1)
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

        # self.tree['height'] = 28  # 设置展示的行数
        # self.tree_1['height'] = 28  # 设置展示的行数
        #
        # self.tree["columns"] = data1[0]
        # self.tree_1["columns"] = data2[0]
        #
        # if len(data1[0]) != len(data2[0]):
        #     print("两个表头列名个数不相同 data1=%s, data2=%s" % (data1[0], data2[0]))
        #
        # for name in data1[0]:
        #     self.tree.column(name, width=10 * 8)  # 设置宽度
        #     self.tree.heading(name, text=name)  # 显示表头
        #
        # for name in data2[0]:
        #     self.tree_1.column(name, width=10 * 8)  # 设置宽度
        #     self.tree_1.heading(name, text=name)  # 显示表头

        self.insert_info_for_tree(data1, data2)

    def insert_info_for_tree(self, data1, data2):

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

        #self.insert_info_for_tree(data1, data2)

        # self.tree.delete(0)
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
