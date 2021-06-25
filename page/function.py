import datetime
import decimal
import tkinter as tk

from Util import dataanalyze
from page.topUiExcel import TopUiExcel, TopUiDeepExcel
from resource import pics
import copy


def get_now_time():
    return datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')


def check_data_by_key(data, excel, data_names, excel_names):
    '''
    :param data: excel的内如： [[], [], ...]
    :param excel: excel的内如： [[], [], ...]
    :param data_names_1: excel第一列的内容 [name1, name2, .....]
    :param data_names_2: excel第一列的内容 [name1, name2, .....]
    :return:
    dif_array: [x1, y1, x2, y2, diff1, diff2]
    dif_row_excel [y, [:]]
    dif_column_excel [x, y, [y-1:]]
    dif_row_data [y, [:]]
    dif_column_data  [x, y, [y-1:]]
    '''
    dif_array, dif_row_excel, dif_column_excel, dif_row_data, dif_column_data = [], [], [], [], []
    len_excel, len_data = len(excel), len(data)
    if len_excel == 1:
        if len_data > 1:
            dif_row_data = [[-1, data]]
        return dif_array, dif_row_excel, dif_column_excel, dif_row_data, dif_column_data
    if len_data == 1:
        if len_excel > 1:
            dif_row_excel = [[-1, excel]]
        return dif_array, dif_row_excel, dif_column_excel, dif_row_data, dif_column_data

    # if len(data_names) != len(data_names):

    col_data, col_excel = len(data[0]), len(excel[0])
    if len(data_names) != 0:
        # todo key列是否会有重复？
        name_data = dict(zip(data_names, range(len(data_names))))
        name_excel = dict(zip(excel_names, range(len(excel_names))))
        for name in list(name_data.keys()):
            i = name_data[name]
            name_ex = name
            if name_ex not in name_excel and str(name_ex) in name_excel:
                name_ex = str(name_ex)

            if name_ex in name_excel:
                col = min(col_data, col_excel)
                for j in range(col):
                    if dif_data(data[i][j], excel[name_excel[name_ex]][j]):
                        continue
                    dif_array.append([i + 1, j + 1, name_excel[name_ex] + 1, j + 1, data[i][j], excel[name_excel[name_ex]][j]])

                if col_data > col:
                    dif_column_data.append([i+1, col+1, data[col:col_data]])
                elif col_excel > col:
                    dif_column_excel.append([i + 1, col + 1, excel[col:col_excel]])

                name_data.pop(name)
                name_excel.pop(name_ex)

        for i in name_data.keys():
            index = name_data[i]
            dif_row_data.append([index, data[index]])

        for i in name_excel.keys():
            index = name_excel[i]
            dif_row_excel.append([index, excel[index]])
    else:
        row = min(len_excel, len_data)
        col = min(col_excel, col_data)
        for i in range(row):
            for j in range(col):
                a, b = data[i][j], excel[i][j]
                if dif_data(a, b):
                    continue
                dif_array.append([i + 1, j + 1, i + 1, j + 1, a, b])

            if col_data > col:
                dif_column_data.append([i + 1, j + 1, data[j:col_data]])
            elif col_excel > col:
                dif_column_excel.append([i + 1, j + 1, excel[j:col_excel]])

        if len_data > row:
            for i in range(row, len_data):
                dif_row_data.append([i, data[i]])
        elif len_excel > row:
            for i in range(row, len_excel):
                dif_row_excel.append([i, excel[i]])

    return dif_array, dif_row_excel, dif_column_excel, dif_row_data, dif_column_data


def filter_by_key(excel_array, data_array, table_key, table_name):

        snap_excel_array = [excel_array[0]]
        snap_data_array = [data_array[0]]
        data_array = copy.deepcopy(data_array)
        excel_array = copy.deepcopy(excel_array)

        for item in ["一列", "二列", "三列"]:
            key = table_key[item]['key']
            rule = table_key[item]['rule']
            value = table_key[item]['value']

            if value == "":
                continue

            if key not in excel_array[0] or key not in data_array[0]:
                raise KeyError("两分表<%s>必须都包含指定key： %s" % (table_name, key))
            index_exl = excel_array[0].index(key)
            index_data = data_array[0].index(key)

            if rule == '包含':
                for _ in data_array:
                    if _ != data_array[0] and value in str(_[index_data]):
                        snap_data_array.append(_)

                for _ in excel_array:
                    if _ != excel_array[0] and value in str(_[index_data]):
                        snap_excel_array.append(_)

            elif rule == "不包含":
                for _ in data_array:
                    if _ != data_array[0] and value not in str(_[index_data]):
                        snap_data_array.append(_)

                for _ in excel_array:
                    if _ != excel_array[0] and value not in str(_[index_data]):
                        snap_excel_array.append(_)

            elif rule == ">":
                for _ in data_array:
                    # todo 这里可能需要value 类型的判断
                    if _ != data_array[0] and int(value) < int(_[index_data]):
                        snap_data_array.append(_)

                for _ in excel_array:
                    if _ != excel_array[0] and int(value) < int(_[index_data]):
                        snap_excel_array.append(_)

            elif rule == "=":
                for _ in data_array:
                    #print("type(value) = %s, value: %s, type(_[index_data]) = %s , _[index_data] = %s" % (type(value), value, type(_[index_data]), _[index_data]))

                    if _ != data_array[0] and (value == _[index_data] or value == str(_[index_data])):
                        snap_data_array.append(_)


                for _ in excel_array:
                    # print("type(value) = %s, value: %s, type(_[index_data]) = %s , _[index_data] = %s" % (
                    # type(value), value, type(_[index_data]), _[index_data]))
                    if _ != excel_array[0] and (value == _[index_data] or value == str(_[index_data]) or value == str(int(_[index_data]))):
                        snap_excel_array.append(_)

            elif rule == "<":
                for _ in data_array:
                    # print("type(value) = %s, value: %s, type(_[index_data]) = %s , _[index_data] = %s" % (type(value), value, type(_[index_data]), _[index_data]))
                    if _ != data_array[0] and int(value) > int(_[index_data]):
                        snap_data_array.append(_)

                for _ in excel_array:
                    if _ != excel_array[0] and int(value) > int(_[index_data]):
                        snap_excel_array.append(_)

            elif rule == '>=':
                for _ in data_array:
                    if _ != data_array[0] and int(value) <= int(_[index_data]):
                        snap_data_array.append(_)

                for _ in excel_array:
                    if _ != excel_array[0] and int(value) <= int(_[index_data]):
                        snap_excel_array.append(_)

            elif rule == '<=':
                for _ in data_array:
                    if _ != data_array[0] and int(value) >= int(_[index_data]):
                        snap_data_array.append(_)

                for _ in excel_array:
                    if _ != excel_array[0] and int(value) >= int(_[index_data]):
                        snap_excel_array.append(_)

            else:
                raise Exception("<%s>中无法识别的key： <%s> %s <%s>" % (table_name, key, rule, value))

            if len(snap_excel_array) != 1 and len(snap_data_array) != 1:
                # print("11111111111111")
                data_array = snap_data_array
                excel_array = snap_excel_array
                snap_excel_array = [excel_array[0]]
                snap_data_array = [data_array[0]]
        return data_array, excel_array


def get_names_by_key(data, key):
    snap = []

    if len(data) < 1 or key not in data[0]:
        return snap
    index = data[0].index(key)

    for item in data:
        snap.append(item[index])

    return snap

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
                if dif_data(data1[i][j], data2[name_2[name]][j]):
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

def dif_data(a, b):
    if a != b:
        # 对于excel全是str情况的的处理
        # 数据库int类型处理
        if isinstance(a, int) and isinstance(b, str):
            try:
                if a == int(b):
                    return True
            except ValueError:
                pass
        # 时间类型处理
        if isinstance(a, datetime.datetime) and isinstance(b, str):
            if str(a) == b:
                return True
        # 时间类型处理
        if isinstance(b, datetime.datetime) and isinstance(a, str):
            if str(b) == a:
                return True
        # 浮点数处理
        if isinstance(a, float) and isinstance(b, str):
            try:
                if a == float(b):
                    return True
            except ValueError:
                pass
        # null处理
        if a == None and b == '':
            return True
        # 科学计数类型处理
        if isinstance(a, decimal.Decimal) and isinstance(b, str):
            try:
                if a == decimal.Decimal(b):
                    return True
            except:
                pass
        # 处理datetime.timedelta类型
        if isinstance(a, datetime.timedelta) and isinstance(b, str):
            try:
                if str(a) == b:
                    return True
            except:
                pass
        try:
            if float(a) == float(b):
                return True
        except:
            pass

        if isinstance(a, str) and isinstance(b, datetime.date):
            try:
                if a == b.strftime('%Y-%m-%d'):
                    return True
            except:
                pass
        if a == '' and b == None:
            return True

        return False
    return True


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
            if dif_data(a, b):
                continue

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


def show_dif_excel(dif_array, dif_row_excel, dif_column_excel, dif_row_data, dif_column_data, table_name, row_name, table_key=None, command=None):
    if command == None:
        data_1, data_2 = dataanalyze.change_dif_data(dif_array, dif_row_excel, dif_column_excel, dif_row_data,
                                                     dif_column_data, row_name)
        TopUiExcel(table_name, data_1, data_2)
    else:
        data_1, data_2 = dataanalyze.change_dif_data_by_key(dif_array, dif_row_excel, dif_column_excel, dif_row_data,
                                                     dif_column_data, row_name)
        TopUiDeepExcel(table_name, data_1, data_2, table_key, row_name, command)


# 打印差异信息到text上
def show_dif_ui(dif_array, dif_row_excel, dif_column_excel, dif_row_data, dif_column_data, tex, table_name='tables',
                row_name=[], table_key=None, commamd=None):
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
                                                                              row_name, table_key, commamd)))

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
        # if dif_column_excel != []:
        #     tex.insert(tk.END, '母文件或数据库二多的列内容：\n')
        #     for key, content in dif_column_excel:
        #         if content != '{}':
        #             tex.insert(tk.END, '<%d列>多余的数据: \n' % key)
        #             for i in content:
        #                 tex.insert(tk.END, i, 'tag2')
        #                 tex.insert(tk.END, '\t')
        #             tex.insert(tk.END, '\n')
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
                tex.insert(tk.END, '(%s行, %s列) %s <---> %s \n' % (each[0], each[1], each[-2], each[-1]), 'tag2')


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
