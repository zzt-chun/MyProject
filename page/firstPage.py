# -*- coding: utf-8 -*-
# @Time    : 2019/11/25 17:19
# @Author  : zzt
# @File    : firstPage.py

import tkinter as tk
from tkinter import ttk
from Util import dataanalyze
import re
from tkinter import filedialog
import os
import datetime
from tkinter import messagebox
import sys
from page.function import show_dif, show_dif_ui, check_datas, check_excels


t_version_rule = [
    'channel',
    'operation',
    'context',
    'min_version',
    'max_version'
]

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
        data_1[self.key_2[0]] = dataanalyze.read_excel_columns(self.path_2[0], self.key_2[0], "t_version")
        data_2[self.key_2[0]] = dataanalyze.read_excel_columns(self.path_2[1], self.key_2[0], "t_version")
        for name in t_version_rule[2:]:
            data_1[name] = dataanalyze.read_excel_columns(self.path_2[0], name, "t_version")
            data_2[name] = dataanalyze.read_excel_columns(self.path_2[1], name, "t_version")
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
            if self.version.sort() == dif_array.sort():
                self.tex.insert(tk.END, self.get_now_time()+':检查通过，所有版本号升级都符合规定\n', 'tag1')
                self.tex.tag_config('tag1', foreground='green')
                for i in dif_array:
                    self.tex.insert(tk.END, i+'\n', 'tag1')
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
        rows_1 = dataanalyze.read_cxcel_rows(self.path_2[0], "t_version")
        rows_2 = dataanalyze.read_cxcel_rows(self.path_2[1], "t_version")
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
        column_1 = dataanalyze.read_excel_columns(self.path_2[0], self.key_2[0], "t_version")
        column_2 = dataanalyze.read_excel_columns(self.path_2[1], self.key_2[1], "t_version")
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

