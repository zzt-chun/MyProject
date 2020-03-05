import xlwt
import datetime
import xlrd

def change_dic(dic):
    '''
    将包含字典的集合转化成包含集合的集合
    '''
    buf = []
    if len(dic) == 0:
        return dic
    buf.append(list(dic[0].keys()))
    for each in dic:
        buf.append(list(each.values()))
    return buf

def change_dic_by_name(dic):
    dic = change_dic(dic)
    _dic = list()
    for _ in dic:
        if _[0] == "column_name":
            continue
        _dic.append(_[0])
    return [_dic]

#保存常规excel文件：内容保存在第一页sheet中的第一列
def write_general_excel(datas, file_name):
    xls = xlwt.Workbook()
    sheet = xls.add_sheet('Tables_list')
    for row in range(len(datas)):
        sheet.write(row, 0, datas[row])
    xls.save(file_name)


def change_dif_data(dif_array, dif_row_excel, dif_column_excel, dif_row_data, dif_column_data, row_name):
    data1, data2 = [], []
    max_row = max(len(row_name[0]), len(row_name[1]))
    data1.append(['列']+row_name[0]+['']*(max_row-len(row_name[0])))
    data2.append(['列']+row_name[1]+['']*(max_row-len(row_name[1])))
    if dif_column_excel != [] or dif_column_data != []:
        try:
            len_excel = len(dif_column_excel[0][1])
        except IndexError:
            len_excel = 0
        try:
            len_data = len(dif_column_data[0][1])
        except IndexError:
            len_data = 0
        for col in range(1, max(len_excel, len_data)):
            buf_1, buf_2 = [col]+['']*max_row, [col]+['']*max_row
            for row, content in dif_column_data:
                buf_1[row+1] = content[col]
            for row, content in dif_column_excel:
                buf_2[row+1] = content[col]
            data1.append(buf_1)
            data2.append(buf_2)
        for x, y, one, two in dif_array:
            data1[x-1][y] = one
            data2[x-1][y] = two
        for x, content in dif_row_data:
            if x >= len(data1):
                data1.append([x]+content+['']*(max_row-len(row_name[0])))
                data2.append([x]+['']*max_row)
            else:
                data1[x][1:] = content
        for x, content in dif_row_excel:
            if x >= len(data2):
                data2.append([x]+content+['']*(max_row-len(row_name[1])))
                data1.append([x] + [''] * max_row)
            else:
                data2[x][1:] = content
    elif dif_array != []:
        for col in range(dif_array[-1][0]):
            buf_1,  buf_2 = [col+1]+['']*max_row, [col+1]+['']*max_row
            data1.append(buf_1)
            data2.append(buf_2)
        buf = list(range(1, 1+dif_array[-1][0]))
        for x, y, one, two in dif_array:
            if x in buf:
                buf.remove(x)
            data1[x][y] = one
            data2[x][y] = two
        for i in buf[::-1]:
            data1.pop(i)
            data2.pop(i)
        for x, content in dif_row_data:
            data1.append([x+1]+content)
            data2.append([x+1]+['']*max_row)
        for x, content in dif_row_excel:
            data2.append([x+1]+content)
            data1.append([x+1]+['']*max_row)
    else:
        for x, content in dif_row_data:
            if x >= len(data1):
                data1.append([x+1]+content+['']*(max_row-len(row_name[0])))
                data2.append([x+1]+['']*max_row)
        for x, content in dif_row_excel:
            if x >= len(data2):
                data2.append([x+1]+content+['']*(max_row-len(row_name[1])))
                data1.append([x + 1] + [''] * max_row)
    return data1, data2

def write_excel(data_array, filename):
    '''
    data_array为一个字典，字典key为sheet名字，值为对应内容
    函数功能为将多个sheet页保存为excel格式文件名为filename
    '''
    if not data_array:
        return False
    xls = xlwt.Workbook()
    sheet = xls.add_sheet('Tables')
    row = 0
    for name in data_array.keys():
        sheet.write(row, 0, row+1)
        sheet.write(row, 1, name)
        row += 1
    key = 1
    for name in data_array.keys():
        try:

            if len(name) >= 31:
                sheet = xls.add_sheet(str(key))
            else:
                sheet = xls.add_sheet(name)
            key += 1
        except Exception as e:
            print(e)
            return False
        col = 0
        style = xlwt.XFStyle()
        style.num_format_str = 'yyyy/m/d h:mm:ss'
        for each_col in data_array[name]:
            row = 0
            for each_row in each_col:
                if type(each_row) == datetime.datetime:
                    sheet.write(col, row, each_row, style)
                else:
                    try:
                        sheet.write(col, row, each_row)
                    except Exception as err:
                        print(err)
                row += 1
            col += 1
    xls.save(filename)
    return True

#获取某sheet某name列内容
def read_excel_columns(path, key, sheet_name=0):
    ex = xlrd.open_workbook(path)
    if isinstance(sheet_name, int):
        sheet = ex.sheet_by_index(0)
    else:
        sheet = ex.sheet_by_name(sheet_name)
    rows = sheet.row_values(0)
    if key not in rows:
        key = float(key)
        if key not in rows:
            return False
    index = rows.index(key)
    return sheet.col_values(index)

#一次性读取母文件及所有表内容
def read_excel_mu_datas(path):
    excelfile = xlrd.open_workbook(path)
    sheet = excelfile.sheet_by_index(0)
    if sheet.ncols != 2:
        return -2
    big_datas = dict()
    names = dict()
    for row in range(sheet.nrows):
        names[sheet.cell_value(row, 1)] = int(sheet.cell_value(row, 0))
    for name in names.keys():
        if 'sheet' in name:
            return -2
    for name in names.keys():
        sheet = excelfile.sheet_by_index(names[name])
        buf = []
        for row in range(sheet.nrows):
            content = []
            for col in range(sheet.ncols):
                if sheet.cell_type(row, col) == 3:
                    content.append(xlrd.xldate_as_datetime(sheet.cell_value(row, col), 0))
                else:
                    content.append(sheet.cell_value(row, col))
            buf.append(content)
        big_datas[name] = buf
    return big_datas

def read_excel_datas(path, index):
    '''
    excelfile = xlrd.open_workbook(path)
    sheet = excelfile.sheet_by_name(name)
    return sheet._cell_values
    '''
    excelfile = xlrd.open_workbook(path)
    if index == None:
        index = 0
    if isinstance(index, str):
        sheet = excelfile.sheet_by_name(index)
    else:
        sheet = excelfile.sheet_by_index(index)
    buf = []
    for row in range(sheet.nrows):
        content = []
        for col in range(sheet.ncols):
            if sheet.cell_type(row, col) ==3:
                content.append(xlrd.xldate_as_datetime(sheet.cell_value(row, col), 0))
            else:
                content.append(sheet.cell_value(row, col))
        buf.append(content)
    return buf

#读取sheet names
def read_excel_sheets(path):
    return xlrd.open_workbook(path).sheet_names()

#读取excel首行names
def read_cxcel_rows(path, name=None):
    ex = xlrd.open_workbook(path)
    if name == None:
        sheet = ex.sheet_by_index(0)
    else:
        sheet = ex.sheet_by_name(name)
    if sheet.ncols < 1:
        return -2
    return sheet.row_values(0)

#读取母文件第一页sheet
def read_excel_names(path):
    excelfile = xlrd.open_workbook(path)
    sheet = excelfile.sheet_by_index(0)
    if sheet.ncols != 2:
        return -2
    names = dict()
    for row in range(sheet.nrows):
        names[sheet.cell_value(row, 1)] = int(sheet.cell_value(row, 0))
    for name in names.keys():
        if 'sheet' in name:
            return -2
    return names
#读取配置文件（table list）
def read_save_names(path):
    excelfile = xlrd.open_workbook(path)
    sheet = excelfile.sheet_by_index(0)
    array = []
    if (sheet.nrows>=500) or (sheet.nrows==0) or (sheet.ncols>=500):
        return -1
    for nrow in range(sheet.nrows):
        for content in sheet.row_values(nrow):
            if content != '' and content not in array:
                array.append(content)
    return array

if __name__ == '__main__':
    '''
    buf = []
    for i in range(10):
        dic = dict()
        for j in ('one', 'two', 'three', 'four', 'five'):
            dic[j] = i
        buf.append(dic)
    buf_1 = dict()
    buf_2 = dict()
    buf_1['list1'] = change_dic(buf)
    buf_1['list2'] = change_dic(buf)
    write_excel(buf_1)
    '''
    array = read_save_names('C:/Users/admin/AppData/Local/Programs/Python/Python37/python_py/test.xls')
    for each in array:
        print(each)
