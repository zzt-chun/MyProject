import datetime
import decimal
import tkinter as tk

from Util import dataanalyze
from page.topUiExcel import TopUiExcel
from resource import pics


def get_now_time():
    return datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')


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
            dif_data1.append('<%d行>多余的数据: \n' % i)
            dif_data1.append(data1[i])
            dif_data1.append('\n')
        else:
            for j in range(min(col_data1, col_data2)):
                if data1[i][j] != data2[name_2[name]][j]:
                    dif_array.append('(%d行, %d列)(%s行， %s列) %s <---> %s \n' % (
                    i + 1, j + 1, name_2[name] + 1, j + 1, data1[i][j], data2[name_2[name]][j]))
            name_2.pop(name)
    for i in name_2.keys():
        dif_data2.append('<%d行>多余的数据: \n' % name_2[i])
        dif_data2.append(data2[name_2[i]])
        dif_data2.append('\n')
    col = min(col_data1, col_data2)
    if col_data2 > col:
        for i in range(col, col_data2):
            dif_data2.append('<%d列>多余的数据: \n' % i)
            for j in range(len_data2):
                dif_data2.append(data2[j][i])
            dif_data2.append('\n')
    elif col_data1 > col:
        for i in range(col, col_data1):
            dif_data1.append('<%d列>多余的数据: \n' % i)
            for j in range(len_data1):
                dif_data1.append(data1[j][i])
            dif_data1.append('\n')
    return dif_array, dif_data1, dif_data2


# 检查两份数据，返回差异部分，dif_array, dif_data, dif_excel
def check_datas(data, excel):
    dif_array, dif_row_excel, dif_column_excel, dif_row_data, dif_column_data = [], [], [], [], []
    len_excel, len_data = len(excel), len(data)
    if not len_excel:
        if len_data:
            dif_row_data = [[1, data]]
        return dif_array, dif_row_excel, dif_column_excel, dif_row_data, dif_column_data
    if not len_data:
        if len_excel > 1:
            dif_row_excel = [[1, excel]]
        return dif_array, dif_row_excel, dif_column_excel, dif_row_data, dif_column_data
    col_excel, col_data = len(excel[0]), len(data[0])
    row = min(len_excel, len_data)
    col = min(col_excel, col_data)
    for i in range(row):
        for j in range(col):
            a, b = data[i][j], excel[i][j]
            if a != b:
                # 对于excel全是str情况的的处理
                # 数据库int类型处理
                if isinstance(a, int) and isinstance(b, str):
                    try:
                        if a == int(b):
                            continue
                    except ValueError:
                        pass
                # 时间类型处理
                if isinstance(a, datetime.datetime) and isinstance(b, str):
                    if str(a) == b:
                        continue
                # 时间类型处理
                if isinstance(b, datetime.datetime) and isinstance(a, str):
                    if str(b) == a:
                        continue
                # 浮点数处理
                if isinstance(a, float) and isinstance(b, str):
                    try:
                        if a == float(b):
                            continue
                    except ValueError:
                        pass
                # null处理
                if a == None and b == '':
                    continue
                # 科学计数类型处理
                if isinstance(a, decimal.Decimal) and isinstance(b, str):
                    try:
                        if a == decimal.Decimal(b):
                            continue
                    except:
                        pass
                # 处理datetime.timedelta类型
                if isinstance(a, datetime.timedelta) and isinstance(b, str):
                    try:
                        if str(a) == b:
                            continue
                    except:
                        pass
                try:
                    if float(a) == float(b):
                        continue
                except:
                    pass
                print('type(a): %s = %s，len(a)=%s'%(a, type(a), len(str(a))))
                print('type(b): %s = %s，len(b)=%s'%(b, type(b), len(str(b))))
                #print('type(b): %s = %s'%(b, type(b)))
                dif_array.append([i + 1, j + 1, a, b])
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
    data_1, data_2 = dataanalyze.change_dif_data(dif_array, dif_row_excel, dif_column_excel, dif_row_data,
                                                 dif_column_data, row_name)
    TopUiExcel(table_name, data_1, data_2)


# 打印差异信息到text上
def show_dif_ui(dif_array, dif_row_excel, dif_column_excel, dif_row_data, dif_column_data, tex, table_name='tables',
                row_name=[]):
    if dif_array == [] and dif_row_excel == [] and dif_column_excel == [] and dif_row_data == [] and dif_column_data == []:
        now_time = get_now_time()
        # now_time = "2019-06-15 11:31:11"
        tex.insert(tk.END, now_time + ': <%s>完全一致\n' % table_name, 'tag1')
        tex.tag_config('tag1', foreground='green')
    else:
        tex.insert(tk.END, '*****************<%s>存在差异*****************' % table_name, 'tag2')
        tex.window_create(tk.END,
                          window=tk.Button(tex, image=pics['tiaozhuan51x27.png'], bd=0, cursor='arrow', bg='#FFFFFF',
                                           command=lambda: show_dif_excel(dif_array, dif_row_excel, dif_column_excel,
                                                                          dif_row_data, dif_column_data, table_name,
                                                                          row_name)))
        tex.insert(tk.END, '\n')
        tex.tag_config('tag2', foreground='red')
        if dif_row_excel != []:
            tex.insert(tk.END, '母文件或数据库二多的行内容：\n')
            for key, content in dif_row_excel:
                if content != '{}':
                    tex.insert(tk.END, '<%d行>多余的数据: \n' % key)
                    for i in content:
                        tex.insert(tk.END, i, 'tag2')
                        tex.insert(tk.END, '\t')
                    tex.insert(tk.END, '\n')
        if dif_column_excel != []:
            tex.insert(tk.END, '母文件或数据库二多的列内容：\n')
            for key, content in dif_column_excel:
                if content != '{}':
                    tex.insert(tk.END, '<%d列>多余的数据: \n' % key)
                    for i in content:
                        tex.insert(tk.END, i, 'tag2')
                        tex.insert(tk.END, '\t')
                    tex.insert(tk.END, '\n')
        if dif_row_data != []:
            tex.insert(tk.END, '线上库或数据库一多的行内容：\n')
            for key, content in dif_row_data:
                if content != '{}':
                    tex.insert(tk.END, '<%d行>多余的数据: \n' % key)
                    for i in content:
                        tex.insert(tk.END, str(i), 'tag2')
                        tex.insert(tk.END, '\t')
                    tex.insert(tk.END, '\n')
        if dif_column_data != []:
            tex.insert(tk.END, '线上库或数据库一多的列内容：\n')
            for key, content in dif_column_data:
                if content != '{}':
                    tex.insert(tk.END, '<%d列>多余的数据: \n' % key)
                    for i in content:
                        tex.insert(tk.END, i, 'tag2')
                        tex.insert(tk.END, '\t')
                    tex.insert(tk.END, '\n')
        if dif_array != []:
            tex.insert(tk.END, '数据不一致部分(默认前者为线上库或数据库一, 后者为母文件或数据库二)： \n')
            for each in dif_array:
                tex.insert(tk.END, '(%s行, %s列) %s <---> %s \n' % (each[0], each[1], each[2], each[3]), 'tag2')


# 打印差异信息到text上
def show_dif(dif_array, dif_data, dif_excel, tex, name='tables'):
    if dif_data == [] and dif_array == [] and dif_excel == []:
        now_time = get_now_time()
        tex.insert(tk.END, now_time + ': <%s>完全一致\n' % name, 'tag1')
        tex.tag_config('tag1', foreground='green')
    else:
        tex.insert(tk.END, '*****************<%s>存在差异*****************\n' % name, 'tag2')
        tex.tag_config('tag2', foreground='red')
        if dif_excel != []:
            tex.insert(tk.END, '母文件或数据库二有多余数据：\n')
            for content in dif_excel:
                if content != '{}':
                    tex.insert(tk.END, content, 'tag2')
            tex.insert(tk.END, '\n')
        if dif_data != []:
            tex.insert(tk.END, '线上库或数据库一有多余数据： \n')
            for content in dif_data:
                tex.insert(tk.END, content, 'tag2')
            tex.insert(tk.END, '\n')
        if dif_array != []:
            tex.insert(tk.END, '数据不一致部分(默认前者为线上库或数据库一, 后者为母文件或数据库二)： \n')
            for content in dif_array:
                tex.insert(tk.END, content, 'tag2')
            tex.insert(tk.END, '\n')
