from tkinter import messagebox
import datetime
import linkdatabase
import dataanalyze
from tkinter import filedialog
import os
import sys
import tkinter as tk
from tkinter import ttk
import time
import re
import subprocess
import threading
import decimal
import configparser
from resource import pics


#用于计数左边按钮数量， 目前最大数量为21， 若超过应相应添加下拉条
menus = []

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
        self.tree.pack(side=tk.TOP)
        self.tree_1.pack(side=tk.TOP)
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
            print("两个表头列名个数不相同 data1=%s, data2=%s"%(data1[0], data2[0]))

        for name in data1[0]:
            self.tree.column(name, width= 10* 8)  # 设置宽度
            self.tree.heading(name, text=name)  # 显示表头

        for name in data2[0]:
            self.tree_1.column(name, width= 10* 8)  # 设置宽度
            self.tree_1.heading(name, text=name)  # 显示表头

        key = 0
        for row in data1:
            if key != 0:
                self.tree.insert('', str(key), values=row)  # 插入数据
            key += 1
        key = 0
        for row in data2:
            if key != 0:
                self.tree_1.insert('', str(key), values=row)  # 插入数据
            key += 1

#多线程启动跑monkey
class MonkeyThread(threading.Thread):
    def __init__(self, shell_command, parent):
        threading.Thread.__init__(self)
        self.thread_stop = False
        self.shell_command = shell_command
        self.parent = parent
    def run(self):
        time.sleep(1)
        ret = ThirdPage.subprocess_check_output(self.parent, self.shell_command)
        ThirdPage.insert_info(self.parent, 'monkey执行完毕', 1, 1)
        ThirdPage.insert_info(self.parent, ret)


def get_now_time():
    return datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')

def show_frame(self):
    for i in menus:
        if i[0] == self:
            if isinstance(i[1], type):
                i[1] = i[1](self)
            self.grid(row=0, column=2)
        else:

            i[0].grid_forget()

def check_excels(data1, data2, data_names_1, data_names_2):
    dif_array = []
    dif_data1 = []
    dif_data2 = []
    len_data1, len_data2 = len(data1), len(data2)
    if len_data1 == 1:
        if len_data2 > 1:
            dif_data2 = data2
        return dif_array, dif_data1, dif_data2
    if len_data2 == 1:
        return dif_array, dif_data1, dif_data2
    name_2 = dict(zip(data_names_2, range(len(data_names_2))))
    col_data1, col_data2 = len(data1[0]), len(data2[0])
    for i in range(len(data_names_1)):
        name = data_names_1[i]
        if name not in name_2:
            dif_data1.append('<%d行>多余的数据: \n'%i)
            dif_data1.append(data1[i])
            dif_data1.append('\n')
        else:
            for j in range(min(col_data1, col_data2)):
                if data1[i][j] != data2[name_2[name]][j]:
                    dif_array.append('(%d行, %d列)(%s行， %s列) %s <---> %s \n' % (i + 1, j + 1, name_2[name]+1, j+1, data1[i][j], data2[name_2[name]][j]))
            name_2.pop(name)
    for i in name_2.keys():
        dif_data2.append('<%d行>多余的数据: \n'%name_2[i])
        dif_data2.append(data2[name_2[i]])
        dif_data2.append('\n')
    col = min(col_data1, col_data2)
    if col_data2 > col:
        for i in range(col, col_data2):
            dif_data2.append('<%d列>多余的数据: \n'%i)
            for j in range(len_data2):
                dif_data2.append(data2[j][i])
            dif_data2.append('\n')
    elif col_data1 > col:
        for i in range(col, col_data1):
            dif_data1.append('<%d列>多余的数据: \n'%i)
            for j in range(len_data1):
                dif_data1.append(data1[j][i])
            dif_data1.append('\n')
    return dif_array, dif_data1, dif_data2


#检查两份数据，返回差异部分，dif_array, dif_data, dif_excel
def check_datas(data, excel):
    dif_array, dif_row_excel, dif_column_excel, dif_row_data, dif_column_data = [], [], [], [], []
    len_excel, len_data = len(excel), len(data)
    if not len_excel:
        if len_data:
            dif_row_data = data
        return dif_array, dif_row_excel, dif_column_excel, dif_row_data, dif_column_data
    if not len_data:
        if len_excel > 1:
            dif_row_excel = excel
        return dif_array, dif_row_excel, dif_column_excel, dif_row_data, dif_column_data
    col_excel, col_data = len(excel[0]), len(data[0])
    row = min(len_excel, len_data)
    col = min(col_excel, col_data)
    for i in range(row):
        for j in range(col):
            a, b = data[i][j], excel[i][j]
            if a != b:
                #对于excel全是str情况的的处理
                #数据库int类型处理
                if isinstance(a, int) and isinstance(b, str):
                    try:
                        if a == int(b):
                            continue
                    except ValueError:
                        pass
                #时间类型处理
                if isinstance(a, datetime.datetime) and isinstance(b, str):
                    if str(a) == b:
                        continue
                #浮点数处理
                if isinstance(a, float) and isinstance(b, str):
                    try:
                        if a == float(b):
                            continue
                    except ValueError:
                        pass
                #null处理
                if a == None and b == '':
                    continue
                #科学计数类型处理
                if isinstance(a, decimal.Decimal) and isinstance(b, str):
                    try:
                        if a == decimal.Decimal(b):
                            continue
                    except:
                        pass
                #处理datetime.timedelta类型
                if isinstance(a, datetime.timedelta) and isinstance(b, str):
                    try:
                        if str(a) == b:
                            continue
                    except:
                       pass
                #print('type(a): %s = %s'%(a, type(a)))
                #print('type(b): %s = %s'%(b, type(b)))
                dif_array.append([i+1, j+1, a, b])
    if len_data > row:
        for i in range(row, len_data):
            dif_row_data.append([i, data[i]])
    elif len_excel > row:
        for i in range(row, len_excel):
            dif_row_excel.append([i, excel[i]])
    if col_data > col:
        for i in range(col, col_data):
            array = []
            for j in range(len_data):
                array.append(data[j][i])
            dif_column_data.append([i, array])
    elif col_excel > col:
        for i in range(col, col_excel):
            array_1 = []
            for j in range(len_excel):
                array_1.append(excel[j][i])
            dif_column_excel.append([i, array_1])
    return dif_array, dif_row_excel, dif_column_excel, dif_row_data, dif_column_data

def show_dif_excel(dif_array, dif_row_excel, dif_column_excel, dif_row_data, dif_column_data, table_name, row_name):
    data_1, data_2 = dataanalyze.change_dif_data(dif_array, dif_row_excel, dif_column_excel, dif_row_data, dif_column_data, row_name)
    TopUiExcel(table_name, data_1, data_2)

#打印差异信息到text上
def show_dif_ui(dif_array, dif_row_excel, dif_column_excel, dif_row_data, dif_column_data, tex, table_name='tables', row_name=[]):
    if dif_array == [] and dif_row_excel == [] and dif_column_excel == [] and dif_row_data == [] and dif_column_data == []:
        now_time = get_now_time()
        tex.insert(tk.END, now_time + ': <%s>完全一致\n' % table_name, 'tag1')
        tex.tag_config('tag1', foreground='green')
    else:
        tex.insert(tk.END, '*****************<%s>存在差异*****************' % table_name, 'tag2')
        tex.window_create(tk.END, window=tk.Button(tex, image=pics['tiaozhuan51x27.png'],bd=0, cursor='arrow', bg='#FFFFFF',command=lambda: show_dif_excel(dif_array, dif_row_excel, dif_column_excel, dif_row_data, dif_column_data, table_name, row_name)))
        tex.insert(tk.END, '\n')
        tex.tag_config('tag2', foreground='red')
        if dif_row_excel != []:
            tex.insert(tk.END, '母文件或数据库二多的行内容：\n')
            for key, content in dif_row_excel:
                if content != '{}':
                    tex.insert(tk.END, '<%d行>多余的数据: \n'%key)
                    for i in content:
                        tex.insert(tk.END, i, 'tag2')
                        tex.insert(tk.END, '\t')
                    tex.insert(tk.END, '\n')
        if dif_column_excel != []:
            tex.insert(tk.END, '母文件或数据库二多的列内容：\n')
            for key, content in dif_column_excel:
                if content != '{}':
                    tex.insert(tk.END, '<%d列>多余的数据: \n'%key)
                    for i in content:
                        tex.insert(tk.END, i, 'tag2')
                        tex.insert(tk.END, '\t')
                    tex.insert(tk.END, '\n')
        if dif_row_data != []:
            tex.insert(tk.END, '目标库或数据库一多的行内容：\n')
            for key, content in dif_row_data:
                if content != '{}':
                    tex.insert(tk.END, '<%d行>多余的数据: \n'%key)
                    for i in content:
                        tex.insert(tk.END, i, 'tag2')
                        tex.insert(tk.END, '\t')
                    tex.insert(tk.END, '\n')
        if dif_column_data != []:
            tex.insert(tk.END, '目标库或数据库一多的列内容：\n')
            for key, content in dif_column_data:
                if content != '{}':
                    tex.insert(tk.END, '<%d列>多余的数据: \n'%key)
                    for i in content:
                        tex.insert(tk.END, i, 'tag2')
                        tex.insert(tk.END, '\t')
                    tex.insert(tk.END, '\n')
        if dif_array != []:
            tex.insert(tk.END, '数据不一致部分(默认前者为目标库或数据库一, 后者为配置表或数据库二)： \n')
            for each in dif_array:
                tex.insert(tk.END, '(%s行, %s列) %s <---> %s \n'%(each[0], each[1], each[2], each[3]), 'tag2')

#打印差异信息到text上
def show_dif(dif_array, dif_data, dif_excel, tex, name='tables'):
    if dif_data == [] and dif_array == [] and dif_excel == []:
        now_time = get_now_time()
        tex.insert(tk.END, now_time + ': <%s>完全一致\n' % name, 'tag1')
        tex.tag_config('tag1', foreground='green')
    else:
        tex.insert(tk.END, '*****************<%s>存在差异*****************\n' % name, 'tag2')
        tex.tag_config('tag2', foreground='red')
        if dif_excel != []:
            tex.insert(tk.END, '配置表或数据库二有多余数据：\n')
            for content in dif_excel:
                if content != '{}':
                    tex.insert(tk.END, content, 'tag2')
            tex.insert(tk.END, '\n')
        if dif_data != []:
            tex.insert(tk.END, '目标库或数据库一有多余数据： \n')
            for content in dif_data:
                tex.insert(tk.END, content, 'tag2')
            tex.insert(tk.END, '\n')
        if dif_array != []:
            tex.insert(tk.END, '数据不一致部分(默认前者为目标库或数据库一, 后者为配置表或数据库二)： \n')
            for content in dif_array:
                tex.insert(tk.END, content, 'tag2')
            tex.insert(tk.END, '\n')


t_version_rule = [
    'channel',
    'operation',
    'context',
    'min_version',
    'max_version'
]

class FunctionPageFrame(tk.Frame):
    '''
    添加功能页面并绑定左边功能按钮
    '''
    def __init__(self, root, first, rb_v, fun=None, text='新功能', b_bg='#2E8B57', ht=600, wh=800, bg=None, photo=None):
        super().__init__(root, height=ht, width=wh, bg=bg)
        self.grid(row=0, column=2)
        tk.Radiobutton(first,
                       text=text,
                       bd=3,
                       indicatoron=False,
                       variable=rb_v,
                       bg=b_bg,
                       value=len(menus)+1,
                       command=lambda: show_frame(self),
                       compound=tk.LEFT,
                       image=photo
                       ).place(relx=0, rely=0.05*len(menus), width=130)
        menus.append([self, fun])

class FirstPage():
    def __init__(self, parent):
        self.parent = parent
        self.sheet = [None, None]
        self.key = [None, None]
        self.path = [None, None]
        self.path_2 = [None, None]
        self.key_2 = [None, None]
        self.top = None
        self.server = None
        self.version = []
        self.creat_buttons()

    def creat_buttons(self):
        self.tapcontrol = ttk.Notebook(self.parent, height=70, width=796)
        self.tab1 = tk.Frame(self.tapcontrol)
        self.tapcontrol.add(self.tab1, text='excel自定义比对')
        self.tab2 = tk.Frame(self.tapcontrol)
        self.tapcontrol.add(self.tab2, text='t_version检查')
        self.tapcontrol.pack(anchor=tk.N)
        #第一分页
        tk.Label(self.tab1, text='表一（xls/xlxs）： ').grid(row=0, column=0, padx=5, pady=1)
        tk.Label(self.tab1, text='表二（xls/xlxs）： ').grid(row=1, column=0, padx=5, pady=1)
        self.entry_1 = tk.StringVar()
        tk.Entry(self.tab1, textvariable=self.entry_1).grid(row=0, column=1, padx=5, pady=1)
        self.entry_1.set('选择或导入')
        self.entry_2 = tk.StringVar()
        tk.Entry(self.tab1, textvariable=self.entry_2).grid(row=1, column=1, padx=5, pady=1)
        self.entry_2.set('选择或导入')
        tk.Button(self.tab1, text='导入', command=lambda: self.import_file_1(self.entry_1, com1, com3, 0)).grid(row=0, column=2, padx=5, pady=1)
        tk.Button(self.tab1, text='导入', command=lambda: self.import_file_1(self.entry_2, com2, com4, 1)).grid(row=1, column=2, padx=5, pady=1)
        com1 = ttk.Combobox(self.tab1, state='readonly')
        com1.bind("<<ComboboxSelected>>", lambda *args: self.set_sheet(com1, com3, 0))
        com1.set('选择sheet(默认不选)')
        com1.grid(row=0, column=3, padx=5, pady=1)
        com2 = ttk.Combobox(self.tab1, state='readonly')
        com2.bind("<<ComboboxSelected>>", lambda *args: self.set_sheet(com2, com4, 1))
        com2.set('选择sheet(默认不选)')
        com2.grid(row=1, column=3, padx=5, pady=1)
        com3 = ttk.Combobox(self.tab1, state='readonly')
        com3.bind("<<ComboboxSelected>>", lambda *args: self.set_key(com3, 0))
        com3.set('选择列名(默认不选)')
        com3.grid(row=0, column=4, padx=5, pady=1)
        com4 = ttk.Combobox(self.tab1, state='readonly')
        com4.bind("<<ComboboxSelected>>", lambda *args: self.set_key(com4, 1))
        com4.set('选择列名(默认不选)')
        com4.grid(row=1, column=4, padx=5, pady=1)
        tk.Button(self.tab1, text='开始对比', command=self.compare_excel, height=3, width=15).grid(row=0, column=5, rowspan=2, padx=6, pady=1)
        #第二页
        tk.Label(self.tab2, text='表一（t_version）').grid(row=0, column=0, padx=5, pady=1)
        tk.Label(self.tab2, text='表二（t_version）').grid(row=1, column=0, padx=5, pady=1)
        self.entry_1_2 = tk.StringVar()
        tk.Entry(self.tab2, textvariable=self.entry_1_2, width=16).grid(row=0, column=1, padx=5, pady=1)
        self.entry_1_2.set('选择或导入')
        self.entry_2_2 = tk.StringVar()
        tk.Entry(self.tab2, textvariable=self.entry_2_2, width=16).grid(row=1, column=1, padx=5, pady=1)
        self.entry_2_2.set('选择或导入')
        tk.Button(self.tab2, text='导入', command=lambda: self.import_file_2(self.entry_1_2, 0)).grid(row=0, column=2, padx=5, pady=1)
        tk.Button(self.tab2, text='导入', command=lambda: self.import_file_2(self.entry_2_2, 1)).grid(row=1, column=2, padx=5, pady=1)
        tk.Label(self.tab2, text='--》').grid(row=0, column=3, padx=5, pady=1, rowspan=2)
        self.com1_2 = ttk.Combobox(self.tab2, state='readonly')
        self.com1_2.bind("<<ComboboxSelected>>", lambda *args: self.set_server(self.com1_2))
        self.com1_2.set('选择区服')
        self.com1_2.grid(row=0, column=4, padx=5, pady=1, rowspan=2)
        tk.Label(self.tab2, text='--》').grid(row=0, column=5, padx=4, pady=1, rowspan=2)
        tk.Button(self.tab2, text='提取版本号', width=13, command=self.get_versions_button).grid(row=0, column=6, padx=4, pady=1, rowspan=2)
        tk.Label(self.tab2, text='--》').grid(row=0, column=7, padx=4, pady=1, rowspan=2)
        tk.Button(self.tab2, text='开始检查', width=13, command=self.check_version).grid(row=0, column=8, padx=4, pady=1, rowspan=2)

        #公用文本
        self.labelf_2 = tk.LabelFrame(self.parent, text='日志文本：')
        self.labelf_2.pack(anchor=tk.N, expand=True)
        sb = tk.Scrollbar(self.labelf_2)
        sb.pack(side=tk.RIGHT, fill=tk.Y)
        self.tex = tk.Text(self.labelf_2, height=33, yscrollcommand=sb.set, width=107)
        self.tex.pack(side=tk.LEFT, fill=tk.BOTH)
        sb.config(command=self.tex.yview)
        tk.Button(self.parent, text='保存日志', command=lambda: self.save_log(self.tex), width=15).pack(anchor=tk.S, side=tk.RIGHT, padx=3, pady=5)
        tk.Button(self.parent, text='清除日志', command=lambda: self.clear_log(self.tex)).pack(anchor=tk.S, side=tk.RIGHT, padx=3, pady=5)

    def check_version(self):
        if None in self.path_2:
            self.tex.insert(tk.END, self.get_now_time()+': 先导入t_version文件\n')
            return
        if self.server == None:
            self.tex.insert(tk.END, self.get_now_time() + ': 先选择区服\n')
            return
        if self.version == []:
            self.tex.insert(tk.END, self.get_now_time() + ': 先提取version内容\n')
            return
        data_1, data_2 = dict(), dict()
        data_1[self.key_2[0]] = dataanalyze.read_excel_columns(self.path_2[0], self.key_2[0])
        data_2[self.key_2[0]] = dataanalyze.read_excel_columns(self.path_2[1], self.key_2[0])
        for name in t_version_rule[2:]:
            data_1[name] = dataanalyze.read_excel_columns(self.path_2[0], name)
            data_2[name] = dataanalyze.read_excel_columns(self.path_2[1], name)
        data_key_1, data_key_2 = dict(), dict()
        for i in range(len(data_1[self.key_2[0]])):
            if data_1[self.key_2[0]][i] == self.server:
                if data_1[t_version_rule[2]][i] != 'MAIN':
                    data_key_1[data_1[t_version_rule[2]][i]] = i
        for i in range(len(data_2[self.key_2[1]])):
            if data_2[self.key_2[1]][i] == self.server:
                if data_2[t_version_rule[2]][i] != 'MAIN':
                    data_key_2[data_2[t_version_rule[2]][i]] = i
        dif_1, dif_1_1, dif_array, dif_2, dif_2_2 = [], [], [], [], []
        for name in data_key_1.keys():
            if name in data_key_2.keys():
                value_1 =float(data_2[t_version_rule[3]][data_key_2[name]]) - float(data_1[t_version_rule[3]][data_key_1[name]])
                value_2 =float(data_2[t_version_rule[4]][data_key_2[name]]) - float(data_1[t_version_rule[4]][data_key_1[name]])
                if value_1 == value_2 == 0:
                    pass
                elif (value_1 >= 1 and value_2 >= 1) or (value_1 <= -1 and value_2 <= -1):
                    dif_array.append(name)
                elif value_1 != 0:
                    dif_1_1.append(name)
                elif value_2 != 0:
                    dif_2_2.append(name)
                data_key_2.pop(name)
            else:
                dif_1.append(name)
        for name in data_key_2.keys():
            dif_2.append(name)
        if dif_1 == dif_2 == dif_1_1 == dif_2_2 == []:
            if self.version == dif_array:
                self.tex.insert(tk.END, self.get_now_time()+':检查通过，所有版本号升级都符合规定\n', 'tag1')
                self.tex.tag_config('tag1', foreground='green')
                for i in dif_array:
                    self.tex.insert(tk.END, i+'\n')
                    return
        self.tex.tag_config('tag2', foreground='red')
        for name in dif_array:
            if name not in self.version:
                self.tex.insert(tk.END, '不应该升级版本号: <%s>\n'%name, 'tag2')
            else:
                self.version.remove(name)
        for name in dif_1:
            if name in self.version:
                self.version.remove(name)
            self.tex.insert(tk.END, '在新版本中被删除的： <%s>\n'%name, 'tag2')
        for name in dif_2:
            if name in self.version:
                self.version.remove(name)
            self.tex.insert(tk.END, '在新版本中是新增的: 《%s》\n'%name, 'tag2')
        for name in dif_1_1:
            if name in self.version:
                self.version.remove(name)
            self.tex.insert(tk.END, '在新版本中“%s”有升级或降低: <%s>\n'%(t_version_rule[3], name), 'tag2')
        for name in dif_2_2:
            if name in self.version:
                self.version.remove(name)
            self.tex.insert(tk.END, '在新版本中“%s”有升级或降低: <%s>\n'%(t_version_rule[4], name), 'tag2')
        for name in self.version:
            self.tex.insert(tk.END, '应该升级版本号，但实际却没有升级的： <%s>\n'%name, 'tag2')


    def get_versions_button(self):
        if self.top != None:
            try:
                self.top.deiconify()
                return
            except :
                self.top = None
        top = tk.Toplevel(width=100, height=100)
        top.title('请输入待识别的内容：')
        self.top = top
        e = tk.Text(top)
        e.pack(expand=True)
        tk.Button(top, text='提取篮球version内容', command=lambda: self.get_version(e.get(1.0, tk.END), 0)).pack(side=tk.RIGHT)
        tk.Button(top, text='提取老足球version内容', command=lambda: self.get_version(e.get(1.0, tk.END), 1)).pack(side=tk.RIGHT)

    def get_version(self, array, index):
        if index == 0:
            p = r"`context` = '([a-z_/]+)'"
        elif index == 1:
            p = r"context = '([A-Z_]+)'"
        self.version = re.findall(p, array)
        if self.version == []:
            self.tex.insert(tk.END, self.get_now_time() + ': 本次提取未提取到任何内容\n')
            self.top.withdraw()
            return
        self.tex.insert(tk.END, self.get_now_time()+': 本次提取的version内容为： \n')
        for each in self.version:
            self.tex.insert(tk.END, each+'\n')
        self.top.withdraw()


    def import_file_2(self, e, index):
        path = filedialog.askopenfilename(filetypes=[('XLSX', '.xlsx'), ('XLS', '.xls')])
        if path == '':
            self.tex.insert(tk.END, self.get_now_time()+': 没有选中导入文件\n')
            return
        self.path_2[index] = path
        e.set(path)
        self.key_2 = [None, None]
        self.server = None
        self.com1_2['values'] = []
        self.com1_2.set('选择区服')
        if None in self.path_2:
            self.tex.insert(tk.END, self.get_now_time()+': 导入<%s>文件成功！\n'%os.path.basename(path))
            self.tex.insert(tk.END, self.get_now_time()+': 目前只导入一份t_version文件，无法选择区服！\n')
            return
        rows_1 = dataanalyze.read_cxcel_rows(self.path_2[0])
        rows_2 = dataanalyze.read_cxcel_rows(self.path_2[1])
        for i in range(2, len(t_version_rule)):
            if t_version_rule[i] not in rows_1 or t_version_rule[i] not in rows_2:
                self.tex.insert(tk.END, self.get_now_time()+': 发现导入文件中存在不包含<%s>字段的情况，请检查是否为合法的t_version文件\n'%t_version_rule[i])
                return
        for i in t_version_rule[:2]:
            if i in rows_1:
                self.key_2[0] = i
            if i in rows_2:
                self.key_2[1] = i
        if None in self.key_2:
            self.tex.insert(tk.END, self.get_now_time() + ': 导入文件中存在不包含<%s>或<%s>, 请检查是否为合法的t_version文件\n' % (
            t_version_rule[0], t_version_rule[1]))
            return
        if self.key_2[0] != self.key_2[1]:
            self.tex.insert(tk.END, self.get_now_time()+': 表一中区服列表名为<%s>， 而表二中的区服列表名为<%s>， 请检查两份表是否为相同项目的t_version文件\n'%(self.key_2[0], self.key_2[1]))
            return
        column_1 = dataanalyze.read_excel_columns(self.path_2[0], self.key_2[0])
        column_2 = dataanalyze.read_excel_columns(self.path_2[1], self.key_2[1])
        server_1, server_2 = [], []
        for i in column_1:
            if i not in server_1:
                server_1.append(i)
        for i in column_2:
            if i not in server_2:
                server_2.append(i)
        if server_1 != server_2 or server_1 == [] or server_2 == []:
            self.tex.insert(tk.END, self.get_now_time()+': 两份表中的区服列名不一致或不存在区服列名情况， 请检查是否为合法的T_version文件\n')
            return
        server_1.remove(self.key_2[0])
        self.com1_2['values'] = server_1
        self.tex.insert(tk.END, self.get_now_time()+': 两份表都合法，请去选择区服\n')

    def set_server(self, com):
        self.server = com.get()
        self.tex.insert(tk.END, self.get_now_time()+': 选择区服<%s>成功\n'%com.get())

    def compare_excel(self):
        if None in self.path:
            self.tex.insert(tk.END, self.get_now_time() + ': 请确认需要比对的文件都已经正确导入\n')
            return
        if self.key[0] != self.key[1]:
            self.tex.insert(tk.END, self.get_now_time() + ': 表一列名《%s》与表二列名《%s》不一致！\n'%(self.key[0], self.key[1]))
            return
        table_names_0 = dataanalyze.read_cxcel_rows(self.path[0], self.sheet[0])
        table_names_1 = dataanalyze.read_cxcel_rows(self.path[1], self.sheet[1])
        is_true = True
        for i in range(min(len(table_names_0), len(table_names_1))):
            if table_names_0[i] != table_names_1[i]:
                is_true = False
                break
        if not is_true:
            self.tex.insert(tk.END, self.get_now_time()+': 目标sheet页中列名不一致， 请检查导入文件的正确性\n')
            self.tex.insert(tk.END, '表一《%s》： %s\n' % (self.sheet[0], table_names_0))
            self.tex.insert(tk.END, '表一《%s》： %s\n' % (self.sheet[1], table_names_1))
            return
        data1 = dataanalyze.read_excel_datas(self.path[0], self.sheet[0])
        data2 = dataanalyze.read_excel_datas(self.path[1], self.sheet[1])
        if None in self.key:
            dif_array, dif_row_excel, dif_column_excel, dif_row_data, dif_column_data = check_datas(data1, data2)
            if len(data1) == 0 or len(data2) == 0:
                self.tex.insert(tk.END, '这里不应该打印！   检查文件存在\n')
                return
            show_dif_ui(dif_array, dif_row_excel, dif_column_excel, dif_row_data, dif_column_data, self.tex, ' and '.join([os.path.basename(self.path[0]), os.path.basename(self.path[1])]), [data1[0], data2[0]])
        else:
            data_key_1 = dataanalyze.read_excel_columns(self.path[0], self.key[0], self.sheet[0])
            data_key_2 = dataanalyze.read_excel_columns(self.path[1], self.key[1], self.sheet[1])
            if False in [data_key_1, data_key_2]:
                self.tex.insert(self.get_now_time() + ': 请检查列名《%s》《%s》是否正确\n'%(self.key[0], self.key[1]))
            dif_array, dif_data, dif_excel = check_excels(data1, data2, data_key_1, data_key_2)
        show_dif(dif_array, dif_data, dif_excel, self.tex, ' and '.join([os.path.basename(self.path[0]),os.path.basename(self.path[1])]))

    def set_key(self, com, index):
        if self.sheet[index] == None:
            com.set('选择列名(默认不选)')
            self.tex.insert(tk.END, self.get_now_time() + ': sheet发生变化，请先选择sheet！\n')
            com['values'] = []
            return
        col = com.get()
        if col == '':
            com.set('选择列名(默认不选)')
            self.tex.insert(tk.END, self.get_now_time()+': 不能选择空白列名！\n')
            self.key[index] = None
            return
        self.key[index] = col
        self.tex.insert(tk.END, self.get_now_time()+': 选择<%s>列作为对比参考列!\n'%col)

    def set_sheet(self, com1, com2, index):
        sheet_name = com1.get()
        rows = dataanalyze.read_cxcel_rows(self.path[index], sheet_name)
        self.sheet[index] = sheet_name
        self.key[index] = None
        if rows == -2:
            self.tex.insert(tk.END, self.get_now_time()+': <%s>分页没有内容，设置失败！\n'%sheet_name)
            com1.set('选择sheet(默认不选)')
            self.sheet[index] = None
            com2['values'] = []
            com2.set('选择列名(默认不选)')
            return
        com2['values'] = rows
        com2.set('选择列名(默认不选)')
        now_time = self.get_now_time()
        self.tex.insert(tk.END, now_time+': 选择<%s>作为对比的sheet页成功！\n'%sheet_name)

    def import_file_1(self, e, com1, com2, index):
        path = filedialog.askopenfilename(filetypes=[('XLSX', '.xlsx'), ('XLS', '.xls')])
        if path == '':
            now_time = self.get_now_time()
            self.tex.insert(tk.END, now_time+': 没有选中导入文件\n')
            return
        self.sheet[index] = None
        self.key[index] = None
        com1.set('选择sheet(默认不选)')
        com2.set('选择列名(默认不选)')
        try:
            com1['values'] = dataanalyze.read_excel_sheets(path)
        except:
            error_buf = sys.exc_info()
            messagebox.showerror(error_buf[0].__name__, error_buf[1])
            com1['values'] = []
            return
        e.set(path)
        self.path[index] = path
        now_time = self.get_now_time()
        self.tex.insert(tk.END, now_time+': <%s>导入成功！\n'%os.path.basename(path))

    def get_now_time(self):
        return datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')

    def clear_log(self, tex):
        tex.delete(1.0, tk.END)


    #保存日志到当前目录（.txt）
    def save_log(self, e):
        array = e.get(1.0, tk.END)
        if len(array) == 1:
            messagebox.showerror('错误', '没有日志可保存!')
            return
        now_time = self.get_now_time()
        if not os.path.exists('配置文件夹'):
            os.mkdir('配置文件夹')
        if not os.path.exists('配置文件夹\日志'):
            os.mkdir('配置文件夹\日志')
        filename = now_time.replace(':', '_')
        filename = ''.join([os.getcwd(), '\配置文件夹\日志\excel日志_', filename, '.txt'])
        with open(filename, 'w') as f:
            f.write(array)
        now_time = self.get_now_time()
        e.insert(tk.END, now_time + ': 日志保存成功, 路径为<%s>\n' % filename)
        messagebox.showinfo('', '保存成功')



#存放服务器信息
servers = dict()

#servers['篮球242'] = "192.168.1.242", "root", "wckj#2017", 3306
#servers['篮球242_1(内网)'] = "192.168.1.242", "nbatest", "DGAG(&Jh23858klh", 3306
servers['篮球201_1(内网)'] = "192.168.1.201", "test", "L*&k34HC98K.kDG%KH", 3307
servers['新足球(内网)'] = "192.168.1.123", "root", "wckj@2017", 3306
servers['老足球(内网)'] = "192.168.1.204", "root", "wckj#2015", 3306
servers['老足球(内网126)'] = "192.168.1.126", "root", "wckj@2018", 3306
servers['中超(内网)'] = "192.168.1.204", "root", "wckj#2015", 3306
#存放活跃数据库对象实例useserver['now'] = xxx
useserver = dict()

class SecondPage():

    def __init__(self, parent):
        self.parent = parent
        self.create_buttons()

    def create_buttons(self):
        tapcontrol = ttk.Notebook(self.parent, height=70, width=796)
        tab1 = tk.Frame(tapcontrol)
        tapcontrol.add(tab1, text='相同版本')
        tab2 = tk.Frame(tapcontrol)
        tapcontrol.add(tab2, text='新老版本')
        tab3 = tk.Frame(tapcontrol)
        tapcontrol.add(tab3, text='版本数据表差异')
        tapcontrol.pack(anchor=tk.N)
        # 第二第一小页
        # 添加选择服务器下拉按钮
        com1 = ttk.Combobox(tab1, state='readonly')
        com1.bind("<<ComboboxSelected>>", lambda *args: self.choose_server(com1, com2, tex))
        com1.set('选择服务器')
        com1['values'] = list(servers.keys())
        com1.grid(row=0, column=0, padx=10, pady=3, rowspan=2)
        # 添加选择数据库下拉按钮
        com2 = ttk.Combobox(tab1, state='readonly')
        com2.bind("<<ComboboxSelected>>", lambda *args: self.choose_database(com2, tex))
        com2.set('选择数据库')
        com2.grid(row=0, column=1, padx=10, pady=3, rowspan=2)
        # 添加文本显示框
        ent1_v = tk.StringVar()
        ent1 = tk.Entry(tab1, textvariable=ent1_v, width=12)
        ent1_v.set('导入配置文件')
        ent1.grid(row=0, column=3, padx=3, pady=1)
        ent2_v = tk.StringVar()
        ent2 = tk.Entry(tab1, textvariable=ent2_v, width=23)
        ent2_v.set('导入母文件')
        ent2.grid(row=1, column=2, padx=3, pady=1, columnspan=2)
        but6 = tk.Button(tab1, text='查看所有表', command=lambda: self.show_tables(tex))
        but6.grid(row=0, column=2, padx=3, pady=1)
        # 添加导入文件按钮
        but1 = tk.Button(tab1, text='导入', command=lambda: self.import_file(ent1_v, tex, True))
        but1.grid(row=0, column=4, padx=3, pady=1)
        but2 = tk.Button(tab1, text='导入', command=lambda: self.import_file(ent2_v, tex, False))
        but2.grid(row=1, column=4, padx=3, pady=1)
        # 添加保存母文件按钮
        ent3_v = tk.StringVar()
        ent3 = tk.Entry(tab1, textvariable=ent3_v, width=12)
        ent3.grid(row=0, column=5, padx=3, pady=1)
        ent3_v.set('自定义文件名')
        but3 = tk.Button(tab1, text='保存母文件', command=lambda: self.save_file(ent1_v, ent3_v, tex), width=12)
        but3.grid(row=0, column=6, padx=3, pady=1)
        but4 = tk.Button(tab1, text='开始检查', command=lambda: self.button_check_file(ent2_v, tex), width=26)
        but4.grid(row=1, column=5, padx=3, pady=1, columnspan=2)
        # 第二页二小页
        com1_2 = ttk.Combobox(tab2, state='readonly')
        com1_2.bind("<<ComboboxSelected>>", lambda *args: self.choose_server(com1_2, [com2_2, com3_2], tex))
        com1_2.set('选择服务器')
        com1_2['values'] = list(servers.keys())
        com1_2.grid(row=0, column=0, padx=20, pady=3, rowspan=2)
        # 添加选择数据库下拉按钮
        com2_2 = ttk.Combobox(tab2, state='readonly')
        com2_2.bind("<<ComboboxSelected>>", lambda *args: self.choose_database(com2_2, tex))
        com2_2.set('选择数据库一')
        com2_2.grid(row=0, column=1, padx=20, pady=3)
        com3_2 = ttk.Combobox(tab2, state='readonly')
        com3_2.bind("<<ComboboxSelected>>", lambda *args: self.choose_database(com3_2, tex))
        com3_2.set('选择数据库二')
        com3_2.grid(row=1, column=1, padx=20, pady=3)
        # 添加文本显示框
        ent1_v_2 = tk.StringVar()
        ent1_2 = tk.Entry(tab2, textvariable=ent1_v_2, width=14)
        ent1_v_2.set('导入配置文件')
        ent1_2.grid(row=0, column=2, padx=3, pady=1, rowspan=2)
        # 添加导入文件按钮
        but1_2 = tk.Button(tab2, text='导入', command=lambda: self.import_file(ent1_v_2, tex, True))
        but1_2.grid(row=0, column=3, padx=3, pady=1, rowspan=2)
        but4_2 = tk.Button(tab2, text='开始检查',
                           command=lambda: self.button_check_data(com2_2.get(), com3_2.get(), ent1_v_2.get(), tex), width=15)
        but4_2.grid(row=0, column=4, padx=3, pady=1, rowspan=2)
        #第二页三小页
        com1_3 = ttk.Combobox(tab3, state='readonly')
        com1_3.bind("<<ComboboxSelected>>", lambda *args: self.choose_server(com1_3, com2_3, tex))
        com1_3.set('选择服务器')
        com1_3['values'] = list(servers.keys())
        com1_3.grid(row=0, column=0, padx=20, pady=3, rowspan=2)
        # 添加选择数据库下拉按钮
        com2_3 = ttk.Combobox(tab3, state='readonly')
        com2_3.bind("<<ComboboxSelected>>", lambda *args: self.choose_database(com2_3, tex))
        com2_3.set('选择数据库')
        com2_3.grid(row=0, column=1, padx=20, pady=3, rowspan=2)
        ent1_v_3 = tk.StringVar()
        ent1_3 = tk.Entry(tab3, textvariable=ent1_v_3, width=28)
        ent1_v_3.set('自定义文件名')
        ent1_3.grid(row=0, column=2, padx=3, pady=1, columnspan=2)
        ent2_v_3 = tk.StringVar()
        ent2_3 = tk.Entry(tab3, textvariable=ent2_v_3, width=20)
        ent2_v_3.set('导入配置表')
        ent2_3.grid(row=1, column=2, padx=3, pady=1)
        but2_3 = tk.Button(tab3, text='导入', command=lambda: self.import_file_table(tex, ent2_v_3))
        but2_3.grid(row=1, column=3, padx=3, pady=1)
        # 添加保存母文件按钮
        but3_3 = tk.Button(tab3, text='保存表list', command=lambda: self.save_table(tex, ent1_v_3), width=15)
        but3_3.grid(row=0, column=4, padx=3, pady=1)
        but4_3 = tk.Button(tab3, text='开始检查', command=lambda: self.check_table_list(tex, ent2_v_3), width=15)
        but4_3.grid(row=1, column=4, padx=3, pady=1)


        # 添加日志文本
        labelf = tk.LabelFrame(self.parent, text='日志文本：')
        labelf.pack(anchor=tk.N, expand=True)
        sb = tk.Scrollbar(labelf)
        sb.pack(side=tk.RIGHT, fill=tk.Y)
        tex = tk.Text(labelf, height=33, yscrollcommand=sb.set, width=107)
        tex.pack(side=tk.LEFT, fill=tk.BOTH)
        sb.config(command=tex.yview)
        # 添加其他按钮
        but5 = tk.Button(self.parent, text='保存日志', command=lambda: self.save_log(tex), width=15)
        but5.pack(anchor=tk.S, side=tk.RIGHT, padx=3, pady=5)
        but7 = tk.Button(self.parent, text='清除日志', command=lambda: self.clear_log(tex))
        but7.pack(anchor=tk.S, side=tk.RIGHT, padx=3, pady=5)

    def import_file_table(self, tex, v):
        path = filedialog.askopenfilename(filetypes=[('XLSX', '.xlsx'), ('XLS', '.xls')])
        if path == '':
            now_time = self.get_now_time()
            tex.insert(tk.END, now_time+': 没有选中导入文件\n')
            return
        v.set(path)
        tex.insert(tk.END, self.get_now_time()+': 导入成功\n')

    def save_table(self, tex, v):
        if len(useserver) == 0:
            now_time = self.get_now_time()
            tex.insert(tk.END, now_time+': 没有选择服务器\n')
            return
        datas = useserver['now'].show_tables()
        if datas == -1:
            now_time = self.get_now_time()
            tex.insert(tk.END, now_time+': 没有选择数据库\n')
            return
        name = v.get()
        if name == '自定义文件名':
            name = ''
        else:
            name = ''.join([name, '_'])
        file_name = ''.join([name, self.get_now_time().replace(':', '_'), '.xlsx'])
        # 数据库格式转化为字符串
        datas = dataanalyze.change_dic(datas)
        datas.pop(0)
        if not os.path.exists('配置文件夹'):
            os.mkdir('配置文件夹')
        if not os.path.exists('配置文件夹\数据库表'):
            os.mkdir('配置文件夹\数据库表')
        file_name = ''.join([os.getcwd(), '\配置文件夹\数据库表\\', file_name])
        dataanalyze.write_general_excel(datas, file_name)
        tex.insert(tk.END, self.get_now_time() + ': 数据库tables list（一共 %d 张表）保存成功, 路径为<%s>\n' % (len(datas), file_name))


    def check_table_list(self, tex, v):
        if len(useserver) == 0:
            now_time = self.get_now_time()
            tex.insert(tk.END, now_time+': 没有选择服务器\n')
            return
        datas = useserver['now'].show_tables()
        if datas == -1:
            now_time = self.get_now_time()
            tex.insert(tk.END, now_time+': 没有选择数据库\n')
            return
        # 数据库格式转化为字符串
        datas = dataanalyze.change_dic(datas)
        datas.pop(0)
        path = v.get()
        if not os.path.isfile(path):
            now_time = self.get_now_time()
            tex.insert(tk.END, now_time+': 没有选择配置表或者文件路径不正确， 请检查\n' )
            return
        datas_2 = dataanalyze.read_excel_datas(path, 0)
        dif_data1, dif_data2 = [], []
        for name in datas_2:
            if name not in datas:
                dif_data2.append(name)
                dif_data2.append('\n')
            else:
                datas.remove(name)
        for name in datas:
            dif_data1.append(name)
            dif_data1.append('\n')
        show_dif([], dif_data1, dif_data2, tex)

    def get_now_time(self):
        return datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')

    def choose_database(self, com2, tex):
        '''
        展示可连接服务器
        :return:
        '''
        if useserver['now'].set_database(com2.get()):
            content = ': 选择数据库<%s>成功\n' % com2.get()
        else:
            content = ': 选择数据库<%s>失败\n' % com2.get()
            com2.set('选择数据库')
        now_time = self.get_now_time()
        tex.insert(tk.END, now_time + content)

    def choose_server(self, com1, com2, tex):
        '''
        展示该服务器下的所有数据库
        必须先选择好服务器
        :return:
        '''
        servername = com1.get()
        ld = linkdatabase.LinkDatabase(*servers[servername])
        if id == None:
            now_time = self.get_now_time()
            tex.insert(tk.END, now_time + ': 选择服务器<%s>失败\n' % servername)
            return
        useserver['now'] = ld
        array = ld.get_databases()
        if array == -1:
            return
        if isinstance(com2, list):
            for com in com2:
                com['values'] = dataanalyze.change_dic(array)
        else:
            com2['values'] = dataanalyze.change_dic(array)
        now_time = self.get_now_time()
        tex.insert(tk.END, now_time+': 选择服务器<%s>成功\n'%servername)

    def show_tables(self, tex):
        if len(useserver) == 0:
            now_time = self.get_now_time()
            tex.insert(tk.END, now_time+': 没有选择服务器\n')
            return
        datas = useserver['now'].show_tables()
        if datas == -1:
            now_time = self.get_now_time()
            tex.insert(tk.END, now_time+': 没有选择数据库\n')
            return
        datas = dataanalyze.change_dic(datas)
        for each in datas:
            tex.insert(tk.END, each[0]+'\n')

    def clear_log(self, tex):
        tex.delete(1.0, tk.END)

    def import_file(self, v, tex, is_save):
        path = filedialog.askopenfilename(filetypes=[('XLSX', '.xlsx'), ('XLS', '.xls')])
        if path == '':
            now_time = self.get_now_time()
            tex.insert(tk.END, now_time+': 没有选中导入文件\n')
            return
        v.set(path)
        if is_save:
            array = dataanalyze.read_save_names(path)
        else:
            array = dataanalyze.read_excel_names(path)
        if array == -1:
            now_time = self.get_now_time()
            tex.insert(tk.END, now_time+': 文件第一页内容为空或超过300行/列，请检查配置文件\n')
            return
        elif array == -2:
            now_time = self.get_now_time()
            tex.insert(tk.END, now_time+': 文件页签不应该包含‘sheet’或其他错误，请检查母文件\n')
            return
        if not is_save:
            array = array.keys()
        for name in array:
            try:
                tex.insert(tk.END, name+'\n')
            except:
                error_buf = sys.exc_info()
                messagebox.showerror(error_buf[0].__name__, error_buf[1])


    def save_file(self, v, v1, tex):
        #保存配置表可能需要一些时间这里应考虑锁屏
        path = v.get()
        if not os.path.isfile(path):
            now_time = self.get_now_time()
            tex.insert(tk.END, now_time+': 没有选择配置表或者文件路径不正确， 请检查\n' )
            return
        if len(useserver) == 0:
            now_time = self.get_now_time()
            tex.insert(tk.END, now_time+': 没有选择服务器\n')
            return
        datas = useserver['now'].show_tables()
        if datas == -1:
            now_time = self.get_now_time()
            tex.insert(tk.END, now_time+': 没有选择数据库\n')
            return
        savenames = dataanalyze.read_save_names(path)
        if savenames == -1:
            now_time = self.get_now_time()
            tex.insert(tk.END, now_time+': 文件第一页内容为空或超过300行/列，请检查配置文件\n')
            return
        #数据库格式转化为字符串
        datas = dataanalyze.change_dic(datas)
        #存放所有数据库表名
        datanames = []
        for name in datas:
            datanames.append(name[0])
        is_continue = True
        for each in savenames:
            if each not in datanames:
                tex.insert(tk.END, '数据库里找不到表<%s>\n'%each)
                is_continue =False
        if not is_continue:
            now_time = self.get_now_time()
            tex.insert(tk.END, now_time+': 配置表有误，保存失败！\n')
            return
        bigdatas = dict()
        for name in savenames:
            datas = useserver['now'].get_table(name)
            if datas == 'no table':
                now_time = self.get_now_time()
                tex.insert(tk.END, now_time + ': 配置表有误，保存失败！\n')
                return
            datas = dataanalyze.change_dic(datas)
            bigdatas[name] = datas
        if not os.path.exists('配置文件夹'):
            os.mkdir('配置文件夹')
        if not os.path.exists('配置文件夹\母文件'):
            os.mkdir('配置文件夹\母文件')
        filename = v1.get()+'_'
        if filename == '自定义文件名_':
            filename = ''
        filename = ''.join([os.getcwd(), '\配置文件夹\母文件\\', filename, '母文件_', get_now_time().replace(':', '_'), '.xlsx'])
        key = dataanalyze.write_excel(bigdatas, filename)
        now_time = self.get_now_time()
        if key:
            tex.insert(tk.END, now_time+': 保存成功, 路径为<%s>\n'%filename)
        else:
            tex.insert(tk.END, now_time+'没东西可保存或表名超过50个字符\n')

    #有效性检查
    def is_valid(self, path, tex):
        if not os.path.isfile(path):
            now_time = self.get_now_time()
            tex.insert(tk.END, now_time + ': 没有选择配置表或者文件路径不正确， 请检查\n')
            return False
        if len(useserver) == 0:
            now_time = self.get_now_time()
            tex.insert(tk.END, now_time + ': 没有选择服务器\n')
            return False
        datas = useserver['now'].show_tables()
        if datas == -1:
            now_time = self.get_now_time()
            tex.insert(tk.END, now_time + ': 没有选择数据库\n')
            return False
        names = dataanalyze.read_excel_names(path)
        if names == -2:
            now_time = self.get_now_time()
            tex.insert(tk.END, now_time + ': 文件页签不应该包含‘sheet’或其他错误，请检查母文件\n')
            return False
        if len(names) >= 300:
            now_time = self.get_now_time()
            tex.insert(tk.END, now_time + ': 需要检查的表数量太多， 超过300个。 操作失败\n')
            return False
        return True

    #用于检查配置表与数据库表的差异
    def button_check_file(self, v, tex):
        path = v.get()
        if not self.is_valid(path, tex):
            return
        datas = useserver['now'].show_tables()
        #time_6 = time.clock()
        names = dataanalyze.read_excel_mu_datas(path)
        #print('一次性读取所有数据花费时间： %f'%(time.clock()-time_6))
        #存放数据库所有表名
        datanames = []
        # 数据库格式转化为字符串
        datas = dataanalyze.change_dic(datas)
        for name in datas:
            datanames.append(name[0])
        is_continue = True
        for each in names.keys():
            if each not in datanames:
                tex.insert(tk.END, '数据库里找不到表<%s>\n'%each)
                is_continue =False
        if not is_continue:
            now_time = self.get_now_time()
            tex.insert(tk.END, now_time+': 配置表有误，检查不通过！\n')
            return
        #index = 1
        for name in names.keys():
            #print('开始检查<%s>'%name)
            #time_1 = time.clock()
            data_array = useserver['now'].get_table(name)
            #time_2 = time.clock()
            #print('从数据库读取花费时间： %f'%(time_2-time_1))
            data_array = dataanalyze.change_dic(data_array)
            #time_3 = time.clock()
            #print('转化数据库数据花费时间： %f'%(time_3-time_2))
            excel_array = names[name]
            #time_4 = time.clock()
            #print('读取某文件花费时间： %f'%(time_4-time_3))
            dif_array, dif_row_excel, dif_column_excel, dif_row_data, dif_column_data = check_datas(data_array, excel_array)
            #time_5 = time.clock()
            #print('比对花费时间： %f'%(time_5-time_4))
            if len(data_array) == 0:
                data_array = ['']
            if len(excel_array) == 0:
                excel_array = ['']
            try:
                show_dif_ui(dif_array, dif_row_excel, dif_column_excel, dif_row_data, dif_column_data, tex, name, [data_array[0], excel_array[0]])
                tex.update()
            except Exception:
                print('data_array = %s'%str(data_array))
                print('excel_array = %s'%str(excel_array))
                return
            #print('第%d个文件检查结束 《%s》,一共花费时间： %f'%(index, name, (time.clock()-time_1)))
            #index += 1
        #print('本次检查花费时间： %f'%(time.clock()-time_6))
    #保存日志到当前目录（.txt）
    def save_log(self, e):
        array = e.get(1.0, tk.END)
        if len(array) == 1:
            messagebox.showerror('错误', '没有日志可保存!')
            return

        filename = self.get_now_time().replace(':', '_')
        if not os.path.exists('配置文件夹'):
            os.mkdir('配置文件夹')
        if not os.path.exists('配置文件夹\日志'):
            os.mkdir('配置文件夹\日志')
        filename = ''.join([os.getcwd(), '\配置文件夹\日志\服务器日志', filename, '.txt'])
        with open(filename, 'w') as f:
            f.write(array)
        now_time = self.get_now_time()
        e.insert(tk.END, now_time + ': 日志保存成功, 路径为<%s>\n' % filename)
        messagebox.showinfo('', '保存成功')

    def button_check_data(self, data1, data2, path, tex):
        # if not self.is_valid(path, tex):
        #     return
        if not useserver['now'].set_database(data1):
            return
        datas_1 = useserver['now'].show_tables()
        names = dataanalyze.read_save_names(path)
        #存放数据库所有表名
        datanames_1 = []
        # 数据库格式转化为字符串
        datas_1 = dataanalyze.change_dic(datas_1)
        for name in datas_1:
            datanames_1.append(name[0])
        #检查数据库一是否都包含目标表
        if not self.check_table(names, datanames_1, data1, tex):
            return
        if not useserver['now'].set_database(data2):
            return
        datas_2 = useserver['now'].show_tables()
        datanames_2 = []
        # 数据库格式转化为字符串
        datas_2 = dataanalyze.change_dic(datas_2)
        for name in datas_2:
            datanames_2.append(name[0])
        if not self.check_table(names, datanames_2, data2, tex):
            return
        for name in names:
            data_content_1 = self.get_data_content(data1, name)
            if data_content_1 == -1:
                return
            data_content_1 = dataanalyze.change_dic(data_content_1)
            data_content_2 = self.get_data_content(data2, name)
            if data_content_2 == -1:
                return
            data_content_2 = dataanalyze.change_dic(data_content_2)
            dif_array, dif_row_excel, dif_column_excel, dif_row_data, dif_column_data = check_datas(data_content_1, data_content_2)
            show_dif_ui(dif_array, dif_row_excel, dif_column_excel, dif_row_data, dif_column_data, tex, name, [data_content_1[0], data_content_2[0]])


    def get_data_content(self, data, name):
        if not useserver['now'].set_database(data):
            return -1
        return useserver['now'].get_table(name)

    #检查数据库一是否都包含目标表
    def check_table(self, names, tables, dataname, tex):

        for each in names:
            if each not in tables:
                tex.insert(tk.END, '<%s>数据库里找不到表<%s>\n'%(dataname, each))
                now_time = self.get_now_time()
                tex.insert(tk.END, now_time + ': 配置表有误,请确认无误后再进行！\n')
                return False
        return True

third_entry_info ={
    '触摸事件(0-100)': [[0, 0], [0, 1, None], '--pct-touch'],
    '手势事件(0-100)': [[1, 0], [1, 1, None], '--pct-motion'],
    '缩放事件(0-100)': [[2, 0], [2, 1, None], '--pct-pinchzoom'],
    '轨迹球事件(0-100)': [[3, 0], [3, 1, None], '--pct-trackball'],
    '屏幕事件(0-100)': [[4, 0], [4, 1, None], '--pct-rotation'],
    '导航事件(0-100)': [[5, 0], [5, 1, None], '--pct-nav'],
    '键盘事件(0-100)': [[0, 2], [0, 3, None], '--pct-flip'],
    '其他事件(0-100)': [[1, 2], [1, 3, None], '--pct-anyevent'],
    '主要事件(0-100)': [[2, 2], [2, 3, None], '--pct-majornav'],
    '系统事件(0-100)': [[3, 2], [3, 3, None], '--pct-syskeys'],
    '切屏事件(0-100)': [[4, 2], [4, 3, None], '--pct-appswitch'],
}

third_label_info = {
    '设备号（必填）': [[0, 0], ['', 0, 1, None], ['获取设备号', 0, 2, None]],
    '待测包(必选)': [[1, 0], ['path', 1, 1, None], ['导入', 1, 2, None]],
    '伪随机值(可选)': [[2, 0], ['path', 2, 1, None], ['修改伪随机', 2, 2, None]],
    '日志等级（必填）': [[3, 0], ['-v-v-v', 3, 1, None], ['修改日志等级', 3, 2, None]],
    '事件数量（必填）': [[4, 0], ['1000', 4, 1, None], ['修改事件数量', 4, 2, None]],
    '延时ms（必填）': [[5, 0], ['100', 5, 1, None], ['修改延时', 5, 2, None]],
}


class ThirdPage():
    def __init__(self, parent):
        self.parent = parent
        self.third_info_command = {
            '设备号（必填）': self.get_device,
            '待测包(必选)': self.get_package_name,
            '伪随机值(可选)': self.set_random_key,
            '日志等级（必填）': self.set_log_level,
            '事件数量（必填）': self.set_event_count,
            '延时ms（必填）': self.set_interval
        }
        self.device_id = None
        self.shell_conmmand = ''
        self.package_name = ''
        self.log_level = ''
        self.event_count = -1
        self.interval = -1
        self.is_run = {'is_alive': None}
        self.random_key = None
        self.create_buttons()

    def create_buttons(self):
        self.parent.pack_propagate(0)
        lf_1 = tk.Frame(self.parent)
        lf_1.grid(row=0, column=0, padx=2)
        for each in third_label_info.keys():
            tk.Label(lf_1, text=each).grid(row=third_label_info[each][0][0], column=third_label_info[each][0][1], padx=3, pady=1)
            third_label_info[each][1][3] = tk.StringVar()
            tk.Entry(lf_1, text=third_label_info[each][1][0], textvariable=third_label_info[each][1][3], width=15).grid(row=third_label_info[each][1][1], column=third_label_info[each][1][2], padx=4, pady=1)
            tk.Button(lf_1, text=third_label_info[each][2][0], width=10, command=self.third_info_command[each]).grid(row=third_label_info[each][2][1], column=third_label_info[each][2][2], padx=5, pady=1)
        lf_2 = tk.LabelFrame(self.parent, text='事件（可选）')
        lf_2.grid(row=0, column=1, pady=5, padx=10)
        for each in third_entry_info.keys():
            tk.Label(lf_2, text=each).grid(row=third_entry_info[each][0][0], column=third_entry_info[each][0][1], padx=3, pady=1)
            third_entry_info[each][1][2] = tk.Entry(lf_2, width=16)
            third_entry_info[each][1][2].grid(row=third_entry_info[each][1][0], column=third_entry_info[each][1][1], padx=3, pady=1)
        lf_3 = tk.Frame(self.parent)
        lf_3.grid(row=1, column=0, columnspan=2, padx=10)
        self.com = ttk.Combobox(lf_3, state='readonly')
        self.com.bind("<<ComboboxSelected>>", self.freed_config)
        self.com.set('选择一键配置')
        self.com.grid(row=0, column=0, padx=10, pady=3)
        self.save_entry = tk.Entry(lf_3, width=12)
        self.save_entry.grid(row=0, column=1)
        self.save_entry.insert(0, '自定义名字')
        tk.Button(lf_3, text='保存配置', width=12, command=self.save_config).grid(row=0, column=2, padx=10, pady=3)
        tk.Button(lf_3, text='开始monkey', width=12, command=self.start_monkey).grid(row=0, column=3, padx=30, pady=3)
        tk.Button(lf_3, text='中断monkey', width=12, command=self.break_monkey).grid(row=0, column=4, padx=30, pady=3)
        labelf = tk.LabelFrame(self.parent, text='日志文本：')
        labelf.grid(row=3, column=0, columnspan=2, padx=10)
        sb = tk.Scrollbar(labelf)
        sb.pack(side=tk.RIGHT, fill=tk.Y)
        self.tex = tk.Text(labelf, height=22, yscrollcommand=sb.set, width=107)
        self.tex.pack(side=tk.LEFT, fill=tk.BOTH)
        sb.config(command=self.tex.yview)
        tk.Button(self.parent, text='清除日志', command=self.clear_log).grid(row=4, column=1, padx=3, pady=3, sticky=tk.E)
        self.tex.tag_config('tag1', foreground='green')
        self.tex.tag_config('tag2', foreground='red')
        self.load_config(self.com)
        if not os.path.exists('配置文件夹'):
            os.mkdir('配置文件夹')
        if not os.path.exists('配置文件夹\monkey日志'):
            os.mkdir('配置文件夹\monkey日志')

    def load_config(self, com):
        cfg = configparser.ConfigParser()
        cfg.read('cfg.ini')
        section_list = cfg.sections()
        if section_list == []:
            self.insert_info('一键配置文件《config.ini》不存在或破损', 1)
        else:
            com['values'] = section_list
            self.insert_info('读取一键配置文件成功！', 1, 1)
            self.insert_info(str(section_list))

    def freed_config(self, *args):
        cfg = configparser.ConfigParser()
        cfg.read('cfg.ini')
        section = self.com.get()
        if section not in cfg.sections():
            self.insert_info('配置<%s>不在配置文件“cfg.ini', 1, 2)
            return
        array = dict(cfg.items(section))
        for name in list(array.keys())[:3]:
            if name not in list(third_label_info.keys())[-3:]:
                self.insert_info('配置文件<%s>异常，不存在《%s》'%(section, name), 1, 2)
                return
            value = array[name]
            if name != '日志等级（必填）' and value != '':
                try:
                     value = int(array[name])
                except ValueError:
                    self.insert_info('<%s> = %s, 配置异常， <%s>的值应为数字'%(name, value, name), 1, 2)
            third_label_info[name][1][3].set(value)
            self.third_info_command[name]()
            self.insert_info('<%s> = "%s"'%(name, value))
        for name in list(array.keys())[3:]:
            if name not in list(third_entry_info.keys()):
                self.insert_info('配置文件<%s>异常，不存在《%s》' % (section, name), 1, 2)
                return
            third_entry_info[name][1][2].delete(0, tk.END)
            third_entry_info[name][1][2].insert(0, array[name])
            self.insert_info('<%s> = "%s" 配置成功！' % (name, array[name]), 1, 1)

    def save_config(self):
        cfg = configparser.ConfigParser()
        cfg.read('cfg.ini')
        section_name = self.save_entry.get()
        if section_name in cfg.sections():
            self.insert_info('自定义名<%s>已存在，保存失败！'%section_name, 1, 2)
            return
        cfg[section_name] = {}
        for name in list(third_label_info.keys())[-3:]:
            cfg[section_name][name] = third_label_info[name][1][3].get()
        for name in list(third_entry_info.keys()):
            cfg[section_name][name] = third_entry_info[name][1][2].get()
        with open('cfg.ini', 'w') as f:
            cfg.write(f)
        self.insert_info('配置<%s>保存成功, 正在重新加载一键配置....'%section_name, 1, 1)
        time.sleep(1)
        self.load_config(self.com)

    def clear_log(self):
        self.tex.delete(1.0, tk.END)

    def get_package_name(self):
        if self.device_id == None:
            self.insert_info('请先获取设备号',1)
            return
        path = filedialog.askopenfilename(filetypes=[('APK', '*.apk')])
        if path == '':
            self.insert_info('没有导入包', 1)
            return
        shell_c = 'aapt dump badging ' + path
        #install = 'adb -s %s install '%self.device_id + path
        p = r"package: name='([a-z.]+)'"
        ret = self.subprocess_check_output(shell_c)
        '''
        buf = ret[:30]
        #用于检查adb命令返回的格式
        buf = buf.replace(' ', "空格")
        buf = buf.replace('\t', "缸t")
        buf = buf.replace('\n', "缸n")
        buf = buf.replace('\r', "缸r")
        self.insert_info("shell = %s"%shell_c, 1, 1)
        self.insert_info("ret = %s"%ret, 1, 1)
        self.insert_info("buf = %s "%buf, 1, 1)
        self.insert_info("日志模式~~~~~", 1, 1)
        '''
        name = re.findall(p, ret)
        if len(name) == 1:
            third_label_info['待测包(必选)'][1][3].set(name[0])
            self.package_name = name[0]
            self.insert_info('被测包名为： %s'%self.package_name)
        else:
            third_label_info['待测包(必选)'][1][3].set('')
            self.insert_info('请检查导入包是否为符合要求的.apk包', 1, 2)
            self.package_name = ''
            return
        self.package_name = name[0]
        #ret = subprocess.getoutput(install)
        #self.insert_info(ret)

    def set_random_key(self):
        value = third_label_info['伪随机值(可选)'][1][3].get()
        try:
            value = int(value)
            if value > 0:
                self.random_key = value
                self.insert_info('<伪随机值>=%s, 修改成功！'%self.random_key, 1, 1)
            else:
                self.insert_info('<伪随机值>不能小于等于0, 请检查', 1, 2)
        except ValueError:
            self.insert_info('<伪随机值>不能为非数字', 1, 2)

    def set_log_level(self):
        value = third_label_info['日志等级（必填）'][1][3].get()
        if value not in ['', '-v', '-v -v', '-v -v -v']:
            self.insert_info('<日志等级>格式不符要求<%s>，请检查'%['', '-v', '-v -v', '-v -v -v'], 1, 2)
            return
        self.log_level = value
        self.insert_info('<日志等级>=%s, 修改成功！' % self.log_level, 1, 1)

    def set_event_count(self):
        value = third_label_info['事件数量（必填）'][1][3].get()
        try:
            value = int(value)
            if value > 0:
                self.event_count = value
                self.insert_info('<事件数量>=%s, 修改成功！'%self.event_count, 1, 1)
            else:
                self.insert_info('<事件数量>不能小于0, 请检查', 1, 2)
        except ValueError:
            self.insert_info('<事件数量>不能为非数字', 1, 2)

    def set_interval(self):
        value = third_label_info['延时ms（必填）'][1][3].get()
        try:
            value = int(value)
            if value > 0:
                self.interval = value
                self.insert_info('<延时ms>=%s, 修改成功！' % self.interval, 1, 1)
            else:
                self.insert_info('<延时ms>不能小于0, 请检查', 1, 2)
        except ValueError:
            self.insert_info('<延时ms>不能为非数字', 1, 2)

    def insert_info(self, information, use_time=0, tag=0):
        if use_time:
            time = get_now_time()+': '
        else:
            time = ''
        if tag == 0:
            this_tag = ''
        elif tag == 1:
            this_tag = 'tag1'
        elif tag == 2:
            this_tag = 'tag2'
        self.tex.insert(tk.END, time+information+'\n', this_tag)

    def break_monkey(self):
        find_monkey_pid = 'adb -s %s shell ps | find "monkey"'%self.device_id
        kill_pid = 'adb -s %s shell kill '%self.device_id
        p = 'shell[ ]+([0-9]+) '
        ret = self.subprocess_check_output(find_monkey_pid)
        pid = re.findall(p, ret)
        if pid == []:
            self.insert_info('没有monkey在运行', 1)
            return
        kill_pid = kill_pid + pid[0]
        ret = self.subprocess_check_output(kill_pid)
        self.insert_info('pid= %s 删除完成'%pid[0], 1, 1)


    def start_monkey(self):
        if self.is_run['is_alive'] != None:
            if self.is_run['is_alive'].isAlive():
                self.insert_info('已经有monkey在运行.....', 1)
                return
        self.shell_conmmand = 'adb'
        if self.device_id == None:
            self.insert_info('请先获取设备号',1)
            return
        else:
            self.shell_conmmand = ''.join([self.shell_conmmand, ' -s %s shell monkey'%self.device_id])

        if self.package_name == '':
            self.insert_info('需要先识别出被测apk包的包体名，用来锁定monkey指令集合都用于被测包', 1)
            return
        else:
            self.shell_conmmand = ''.join([self.shell_conmmand, ' -p %s'%self.package_name])
        if self.log_level not in ['', '-v', '-v -v', '-v -v -v']:
            self.insert_info('<日志等级>不符要求<%s>，请检查'%['', '-v', '-v -v', '-v -v -v'], 1, 2)
            return
        else:
            self.shell_conmmand = ''.join([self.shell_conmmand, ' %s'%self.log_level])
        try:
            self.event_count = int(self.event_count)
            if self.event_count <= 0:
                self.insert_info('<事件数量>不能小于0或为空')
                return
        except ValueError or TypeError:
            self.insert_info('<事件数量>不能为非数字： '%self.event_count, 1, 2)
            return
        try:
            self.interval = int(self.interval)
            if self.interval <= 0:
                self.insert_info('<延时ms> 不能为小于0或为空',1)
                return
            self.shell_conmmand = ''.join([self.shell_conmmand, ' --throttle %d'%self.interval])
        except ValueError:
            self.insert_info('<延时ms>不能为非数字： '%self.interval,1)
            return
        total = 0
        is_continue = True
        for name in third_entry_info.keys():
            value = third_entry_info[name][1][2].get()
            try:
                value = int(value)
                if 0 <= value <= 100:
                    self.shell_conmmand = ''.join([self.shell_conmmand, ' %s %d'%(third_entry_info[name][2], value)])
                    total += value
                else:
                    self.insert_info('<%s>不能超过100或小于0'%name,1, 2)
                    is_continue = False
            except ValueError:
                if value.strip() != '':
                    self.insert_info('<%s>不能为非数字： %s'%(name, value),1, 2)
                    is_continue = False
        if is_continue:
            if total > 100:
                self.insert_info('所有事件总和不能超过100', 1, 2)
                return
            else:
                if self.random_key == None:
                    send = ''
                else:
                    send = ' -s %s'%self.random_key
                filename = get_now_time().replace(':', '_')
                filename = filename.replace(' ', '_')
                self.shell_conmmand = ''.join([self.shell_conmmand,  send, ' %s' % self.event_count, ' >%s'%os.getcwd(), '\配置文件夹\monkey日志\monkey', filename, '.txt'])
                self.insert_info('正在启动monkey.....', 1, 1)
                self.insert_info('执行过程中，可随时中断', 1, 1)
                self.insert_info(self.shell_conmmand)
                tt = MonkeyThread(self.shell_conmmand, self)
                self.is_run['is_alive'] = tt
                tt.start()

    def get_device(self):
        ret = self.subprocess_check_output('adb devices')
        p = r'List of devices attached\r\n([a-z0-9A-Z]+)\tdevice\r\n'
        dev = re.findall(p, ret)
        if dev == []:
            # attached之后增加“[ ]+”是发现有些机器会多一个空格
            p = r'List of devices attached[ ]+\r\n([a-z0-9A-Z]+)\tdevice\r\n'
            dev = re.findall(p, ret)
            if dev == []:
                self.insert_info('获取设备号失败！', 1, 2)
                self.insert_info(ret)
                third_label_info['设备号（必填）'][1][3].set('')
                self.device_id = None
                return
        if len(dev) == 1:
            self.insert_info('获取设备号成功！', 1, 1)
            third_label_info['设备号（必填）'][1][3].set(dev)
            self.device_id = dev[0]
        else:
            self.device_id = None
            self.insert_info('这里不应该被执行')


    #subprocess.getoutput()在打包“-w”后会出现subprocess无效问题而采用subprocess.Popen（）函数
    def subprocess_check_output(self, *args):
        p = subprocess.Popen(*args, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        msg = ''
        for line in p.stdout.readlines():
            msg += line.decode('utf-8')
        status = p.wait()
        return msg

class FifthPage():
    def __init__(self, parent):
        self.parent = parent
        self.create_buttons()
        self.is_line = False
        self.dev_ip = None
        self.dev_id = None
        self.dev_port = None

        self.image_save_path = os.getcwd()+"\配置文件夹\截屏"

    def create_buttons(self):
        self.parent.pack_propagate(0)
        f0 = tk.Frame(self.parent)
        f0.pack(anchor=tk.N, expand=True)
        tk.Label(f0, text="先USB连接手机").grid(row=0, column=0, rowspan=2, padx=5, pady=30)
        tk.Button(f0, text="获取手机ip", command=self.get_device_ip, width=10).grid(row=0, column=1, rowspan=2, padx=5, pady=10)
        self.ent_1 = tk.StringVar()
        tk.Entry(f0, textvariable=self.ent_1, width=10).grid(row=0, column=2, rowspan=2, padx=5, pady=30)
        self.ent_1.set("端口")
        tk.Button(f0, text="绑定端口", command=self.bing_port, width=10).grid(row=0, column=3, rowspan=2, padx=5, pady=10)
        tk.Button(f0, text="连接手机", command=self.connect_device, width=10).grid(row=0, column=4, padx=5, pady=10)
        tk.Button(f0, text="断开连接", command=self.disconnect_device, width=10).grid(row=1, column=4, padx=5, pady=5)
        tk.Button(f0, text="一键截屏并保存到电脑", command=self.save_screen, width=18, height=3).grid(row=0, column=5, rowspan=2, padx=5, pady=15)
        tk.Button(f0, text="一键安装包", command=self.install_package, width=16).grid(row=0, column=6, padx=5, pady=10)
        tk.Button(f0, text="打开图片文件夹", command=self.open_image, width=16).grid(row=1, column=6, padx=5, pady=5)
        #日志文本
        labelf = tk.LabelFrame(self.parent, text='日志文本：')
        labelf.pack(anchor=tk.S, expand=True)
        sb = tk.Scrollbar(labelf)
        sb.pack(side=tk.RIGHT, fill=tk.Y)
        self.tex = tk.Text(labelf, height=33, yscrollcommand=sb.set, width=107)
        self.tex.pack(side=tk.LEFT, fill=tk.BOTH)
        sb.config(command=self.tex.yview)
        self.tex.tag_config('tag1', foreground='green')
        self.tex.tag_config('tag2', foreground='red')
        # 添加其他按钮
        tk.Button(self.parent, text='清除日志', command=lambda: self.tex.delete(1.0, tk.END)).pack(anchor=tk.S, side=tk.RIGHT, padx=5, pady=5)
        if not os.path.exists('配置文件夹'):
            os.mkdir('配置文件夹')
        if not os.path.exists('配置文件夹\截屏'):
            os.mkdir('配置文件夹\截屏')

    def bing_port(self):
        if self.dev_ip == None:
            self.insert_info("请先获取手机ip", 1)
            self.dev_port = None
            return
        #绑定手机端口 adb tcpip ip：port
        port = self.ent_1.get()
        if not port.isdigit():
            self.insert_info("<%s>端口号不符要求， 只能包含数字，请检查！"%port, 1, 2)
            self.dev_port = None
            return
        else:
            self.dev_port = port
        shell_bing_ip = "adb -s %s tcpip %s"%(self.dev_id, self.dev_port)
        ret = self.subprocess_check_output(shell_bing_ip)
        if ret == '':
            self.insert_info("绑定ip=%s 的端口《%s》成功！"%(self.dev_ip, self.dev_port), 1, 1)
        else:
            self.insert_info(ret)
            self.dev_port = None

    def get_device_ip(self):
        ret = self.subprocess_check_output('adb devices')
        p = r'List of devices attached\r\n([a-z0-9A-Z]+)\tdevice'
        dev = re.findall(p, ret)
        if dev == []:
            # attached之后增加“[ ]+”是发现有些机器会多一个空格
            p = r'List of devices attached[ ]+\r\n([a-z0-9A-Z]+)\tdevice'
            dev = re.findall(p, ret)
            if dev == []:
                self.insert_info('获取设备号失败！, 请检查手机是否已经通过usb连接成功或已经正确打开开发者模式。', 1, 2)
                self.insert_info(ret)
                '''
                用于检查adb命令返回的格式
                ret = ret.replace(' ', "空格")
                ret = ret.replace('\t', "缸t")
                ret = ret.replace('\n', "缸n")
                ret = ret.replace('\r', "缸r")
                self.insert_info(ret)
                '''
                self.dev_id = None
                return
        if len(dev) == 1:
            self.dev_id = dev[0]
            self.insert_info('获取设备号成功！ id = %s'%self.dev_id, 1, 1)
        else:
            self.insert_info("获取设备号失败， 这里不应该被打印。", 1, 2)
            self.dev_id = None
        #获取手机ip
        shell_get_ip = "adb -s %s shell ifconfig wlan0"%self.dev_id
        ret = self.subprocess_check_output(shell_get_ip)
        p = r"inet addr:([0-9.]+) "
        dev_ip = re.findall(p, ret)
        if dev_ip == []:
            self.insert_info("获取手机ip失败", 1, 2)
            self.insert_info(ret)
            self.dev_ip = None
            return
        elif len(dev_ip) == 1:
            self.dev_ip = dev_ip[0]
            self.insert_info("获取手机ip成功： ip = %s"%self.dev_ip, 1, 1)
        else:
            self.insert_info("获取手机ip失败， 这里不应该被打印。", 1, 2)
            self.dev_id = None

    def open_image(self):
        shell = r"start explorer %s"%self.image_save_path
        os.system(shell)

    def connect_device(self):
        if not self.dev_port:
            self.insert_info("请先绑定端口", 1)
            return
        p = r"[0-9]+.[0-9]+.[0-9]+.[0-9]+"
        ip = re.findall(p, self.dev_ip)
        if ip == []:
            self.insert_info("<%s>格式不符合要求，请检查"%self.dev_ip, 1, 2)
            return
        # wifi连接手机 adb connect 192.168.10.143:5555
        connect_wifi = "adb -s %s connect %s:%s"%(self.dev_id, self.dev_ip, self.dev_port)
        ret = self.subprocess_check_output(connect_wifi)
        if "failed" in ret:
            self.insert_info("<%s>连接失败"%connect_wifi, 1, 1)
            self.is_line = False
        else:
            self.insert_info(ret, 1, 1)
            self.insert_info("已经通过wifi连接手机成功， 可以拔掉连接usb接口的数据线了", 1, 1)
            self.is_line = True

    def disconnect_device(self):
        if not self.dev_port:
            self.insert_info("请先绑定端口", 1)
            return
        p = r"[0-9]+.[0-9]+.[0-9]+.[0-9]+"
        ip = re.findall(p, self.dev_ip)
        if ip == []:
            self.insert_info("<%s>格式不符合要求，请检查"%self.dev_ip, 1, 2)
            return
        # wifi断开手机 adb disconnect 192.168.10.143:5555
        connect_wifi = "adb disconnect %s:%s"%(self.dev_ip, self.dev_port)
        ret = self.subprocess_check_output(connect_wifi)
        if ret == '':
            self.insert_info("《%s:%s》该连接不存在"%(self.dev_ip, self.dev_port), 1, 2)
        else:
            self.insert_info(ret, 1, 1)
            self.is_line = False

    def install_package(self):
        if not self.is_line:
            self.insert_info("请先连接手机", 1)
            return
        path = filedialog.askopenfilename(filetypes=[('APK', '*.apk')])
        if path == '':
            self.insert_info('没有导入包', 1)
            return
        # 安装apk包
        akp_size = os.path.getsize(path)
        install_apk = "adb -s %s:%s install %s"%(self.dev_ip, self.dev_port, path)
        self.insert_info("正常传输文件....", 1, 1)
        self.insert_info("文件较大可能需要继续等待.....", 1, 1)
        self.insert_info("部分机型需要在手机端手动确认是否安装包.....", 1, 1)
        self.tex.see(tk.END)
        self.tex.update()
        ret = self.subprocess_check_output(install_apk)
        self.insert_info(ret, 1, 1)

    def save_screen(self):
        if not self.is_line:
            self.insert_info("请先连接手机", 1)
            return
        #截屏
        scr = "adb -s %s:%s shell /system/bin/screencap -p /sdcard/screenshot.jpg"%(self.dev_ip, self.dev_port)
        ret_1 = self.subprocess_check_output(scr)
        # 从手机把图片保存到电脑
        image_name = get_now_time().replace(':', '_')
        image_name = image_name.replace(' ', '_')
        get_iamge = "adb -s %s:%s pull /sdcard/screenshot.jpg %s\%s.jpg"%(self.dev_ip, self.dev_port, self.image_save_path, image_name)
        ret_2 = self.subprocess_check_output(get_iamge)
        self.insert_info(ret_2, 1, 1)

    def subprocess_check_output(self, *args):
        p = subprocess.Popen(*args, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        msg = ''
        for line in p.stdout.readlines():
            msg += line.decode('utf-8')
        status = p.wait()
        return msg

    def insert_info(self, information, use_time=0, tag=0):
        if use_time:
            time = get_now_time()+': '
        else:
            time = ''
        if tag == 0:
            this_tag = ''
        elif tag == 1:
            this_tag = 'tag1'
        elif tag == 2:
            this_tag = 'tag2'
        self.tex.insert(tk.END, time+information+'\n', this_tag)

