import os
import sys
from PyQt5 import QtCore, QtGui, QtWidgets

from Util import dataanalyze
from Util.dataanalyze import dif_data
import datetime

class MyThread(QtCore.QThread):
    data_signal = QtCore.pyqtSignal(list, list, list, list)
    info_signal = QtCore.pyqtSignal(list, list, list, list, list)

    def __init__(self, fun):
        super().__init__()
        self.func = fun
        self.is_on = False

    def run(self):
        self.is_on = True
        dif_array, dif_row_excel, dif_column_excel, dif_row_data, dif_column_data, data1, data2 = self.func()
        # print("data1: ", data1)
        # print("data2: ", data2)
        if data2 == ['']:
            data2 = [[], []]
        self.data_signal.emit(data1[1:], data2[1:], data1[0], data2[0])
        self.info_signal.emit(dif_array, dif_row_data, dif_column_data, dif_row_excel, dif_column_excel)
        self.is_on = False

class BuildPackage(object):

    def __init__(self):
        self.is_red = False
        self.cache = ""
        self.final_package = ""

    def insert(self, char, is_diff=False):
        if is_diff == self.is_red:
            self.cache = "".join([self.cache, char])
        else:
            if self.cache:
                self.final_package = "".join([self.final_package, self.build_label_content(self.cache, self.is_red)])
            self.is_red = is_diff
            self.cache = char

    def get_complete_package(self):
        return self.final_package if not self.cache else "".join([self.final_package, self.build_label_content(self.cache, self.is_red)])

    @classmethod
    def build_label_content(cls, _str, is_red=False, is_green=False):
        if not _str:
            return _str
        coloc_sheet = ""
        if is_red:
            coloc_sheet = "color=\'#FF0000\'"
        elif is_green:
            # coloc_sheet = "color=lime"
            coloc_sheet = "color=\'#319400\'"
        return f'''<font {coloc_sheet} size=5>{_str}</font>'''

# class Table(QtWidgets.QMainWindow):
class Table(object):

    relation = ['>', '=', '<', '>=', '<=', "包含", '不包含']
    definition = ["一列", "二列", "三列", "key", "rule", "value", "table_key"]

    def __init__(self, table_name, table_key, names, comand):
        # print("table_name: ", table_name)
        # print("table_key: ", table_key)
        # print("names: ", names)
        # print("comand: ", comand)
        self.father = comand.qt
        self.father.setWindowTitle("表格")
        self.father.resize(1800, 950)
        self.father.move(80, 40)
        self.table_name = table_name
        self.diff_controller = comand
        # self.table_key = table_key
        self.names: [str, str] = names[0]
        self.isReset = True
        self.rules = {}
        self.init_ui()
        self.reset_rules(table_key)
        self.father.show()
        self.thread = MyThread(self._deep_diff)
        self.thread.data_signal.connect(self.inset_data)
        self.thread.info_signal.connect(self.set_table_color)
        self.next_index = -1
        self.diff_record = None
        self.len_diff = 0

    def init_ui(self):
        self.create_top_central_group_box()
        self.create_top_right_group_box()
        self.create_top_left_group_box()
        self.create_bottom_group_box()

        self.main_widget = QtWidgets.QWidget()  # 创建窗口主部件
        self.main_layout = QtWidgets.QVBoxLayout()  # 创建主部件的垂直布局
        self.main_layout.setSpacing(10)


        self.topLayout = QtWidgets.QHBoxLayout()  # 上方布局
        self.bottomLayout = QtWidgets.QGridLayout()  # 下方布局
        # self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 隐藏边框
        self.topLayout.addWidget(self.top_left_group_box)  # top局添加一组box
        self.topLayout.addWidget(self.top_central_group_box)  # top布局添加另一组box
        self.topLayout.addWidget(self.top_right_group_box)  # top布局添加另一组box
        self.bottomLayout.addWidget(self.bottom_group_box) # top布局添加另一组box
        self.main_layout.addLayout(self.topLayout)  # 主布局添加top布局
        self.main_layout.addLayout(self.bottomLayout)  # 也可以不创建上面下方布局，直接addWidget液效果相同

        self.main_widget.setLayout(self.main_layout)  # 设置窗口主部件布局为网格布局
        self.father.setCentralWidget(self.main_widget)  # 设置窗口主部件

        self.inset_data(
            self.diff_controller.get_left_content()[1:],
            self.diff_controller.get_right_content()[1:],
            self.diff_controller.get_left_table_head(),
            self.diff_controller.get_right_table_head(),
        )

    def create_top_left_group_box(self):
        self.top_left_group_box = QtWidgets.QGroupBox("功能：")
        self.gridLayout = QtWidgets.QGridLayout()
        label_2 = QtWidgets.QLabel("选择基准key：")
        self.top_left_combox = QtWidgets.QComboBox()
        self.top_left_combox.addItems(["筛选条件"] + self.names)
        self.top_left_combox.currentIndexChanged.connect(
            lambda *args: self.choose_key(self.top_left_combox, 0, self.definition[6]))
        # self.top_left_combox.addItems(['41', '42', '43'])
        self.buttom_deep_diff = QtWidgets.QPushButton("深度比对")
        self.buttom_deep_diff.clicked.connect(lambda: self.deep_diff())
        self.buttom_reset = QtWidgets.QPushButton("重置条件")
        self.buttom_reset.clicked.connect(lambda: self.reset_rules())
        self.button_next = QtWidgets.QPushButton("next")
        self.button_next.clicked.connect(lambda: self.go_next())
        self.button_save = QtWidgets.QPushButton("保存规则至母文件")
        self.button_save.clicked.connect(lambda: self.save())

        # self.top_layout.addWidget(self.left_close, 0, 3)
        # self.top_layout.addWidget(self.left_visit, 0, 1)
        # self.top_layout.addWidget(self.left_mini, 0, 2)

        self.gridLayout.addWidget(label_2, 0, 0)
        self.gridLayout.addWidget(self.top_left_combox, 0, 1)
        self.gridLayout.addWidget(self.buttom_deep_diff, 1, 0)
        self.gridLayout.addWidget(self.button_next, 1, 1)
        self.gridLayout.addWidget(self.button_save, 2, 1)
        self.gridLayout.addWidget(self.buttom_reset, 2, 0)
        self.gridLayout.setSpacing(12)

        self.top_left_group_box.setLayout(self.gridLayout)
        self.top_left_group_box.setMaximumSize(320, 180)

    def save(self):
        m = QtWidgets.QFileDialog.getOpenFileName(None,"选取文件夹", "./", "XLS Files (*.xls);;XLSX Files (*.xlsx)")  # 起始路径
        if not m[0]:
            self.insert_info("没有选中导入文件", 1, 1)
            return
        self.insert_info("选择的路径： %s" % m[0], 1, 1)
        if not os.path.exists(m[0]):
            self.insert_info("目标路径不存在： %s" % m[0])
            return

        self.rules[self.definition[0]][self.definition[5]] = self.text_1_2.text()
        self.rules[self.definition[1]][self.definition[5]] = self.text_2_2.text()
        self.rules[self.definition[2]][self.definition[5]] = self.text_3_2.text()
        if self.rules[self.definition[2]][self.definition[5]] != "":
            self.rules[self.definition[2]][self.definition[4]] = self.conbox_3_1.currentText()
        if self.rules[self.definition[1]][self.definition[5]] != "":
            self.rules[self.definition[1]][self.definition[4]] = self.conbox_2_1.currentText()
        if self.rules[self.definition[0]][self.definition[5]] != "":
            self.rules[self.definition[0]][self.definition[4]] = self.conbox_1_1.currentText()
        try:
            result = dataanalyze.modifyExcel(m[0], [self.table_name, self.rules])
        except Exception as e:
            self.insert_info(str(e), 1, 2)
            return
        if not result[0]:
            self.insert_info(result[1], 1, 2)
        else:
            self.insert_info("保存成功： %s" % m[0], 1, 1)


    def go_next(self):
        if not self.len_diff:
            self.insert_info("两份表中相同位置没有差异，请拉到最右/最底部查看表1/表2多余数据")
            return
        self.next_index += 1
        if self.next_index >= self.len_diff:
            self.next_index -= self.len_diff
        item = self.diff_record[self.next_index]
        y_offset = -1 if self.isReset else 0
        self.TableWidget_left.setCurrentCell(
            item[0] - 2,
            item[1] + y_offset,
        )
        # 切换光标到左表
        self.TableWidget_left.setFocus()
        self.left_control_right()



    def reset_rules(self, data=None):
        self. rules = data or {
                self.definition[0]: {self.definition[3]: '', self.definition[4]: '', self.definition[5]: ''},
                self.definition[1]: {self.definition[3]: '', self.definition[4]: '', self.definition[5]: ''},
                self.definition[2]: {self.definition[3]: '', self.definition[4]: '', self.definition[5]: ''},
                self.definition[6]: '',
            }
        self.reset_button()
        self.isReset = False if data else True
        self.insert_info("初始化成功", 1, 1)




    def insert_info(self, information, use_time=0, tag=0):
        if use_time:
            time = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S') + ': '
        else:
            time = ''
        is_red = False
        is_green = False
        if tag == 2:
            is_red = True
        elif tag == 1:
            is_green = True
        self.log_text.append(
            BuildPackage.build_label_content(time + information, is_red, is_green)
        )


    def create_top_right_group_box(self):
        self.top_right_group_box = QtWidgets.QGroupBox("日志：")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.log_text = QtWidgets.QTextEdit()
        self.gridLayout_2.addWidget(self.log_text, 0, 0)

        self.top_right_group_box.setLayout(self.gridLayout_2)
        # self.top_right_group_box.setMaximumSize(620, 180)
        self.top_right_group_box.setMaximumSize(720, 220)

    def create_bottom_group_box(self):
        self.bottom_group_box = QtWidgets.QGroupBox("diff： %s" % self.table_name)
        self.gridLayout_3 = QtWidgets.QGridLayout()
        # max_width = max(len(self.diff_controller.get_right_table_head()), len(self.diff_controller.get_left_table_head()))
        # max_heigth =max(len(self.diff_controller.get_right_content()), len(self.diff_controller.get_left_content()))
        # self.TableWidget_left = QtWidgets.QTableWidget(max_heigth, max_width)
        self.TableWidget_left = QtWidgets.QTableWidget()
        # self.TableWidget_right = QtWidgets.QTableWidget(max_heigth, max_width)
        self.TableWidget_right = QtWidgets.QTableWidget()

        self.left_label_2 = QtWidgets.QLabel("目标库: (通过为数据库,数据行号从0开始,实际行号需要减一)")
        self.left_label_3 = QtWidgets.QLabel("参考库: (常为母文件excel，数据行号从1开始且首行会算一行，实际行号需要加一)")
        # 单元格diff内容展示
        self.diff_label_left = QtWidgets.QLabel()
        self.diff_label_left.setWordWrap(True)
        self.diff_label_right = QtWidgets.QLabel()
        self.diff_label_right.setWordWrap(True)
        self.diff_label_left.setStyleSheet('border-width: 2px;border-style: solid;' 
                                           'border-color: rgb(255, 170, 0);'
                                           'background-color:rgb(253, 245, 230);')
        self.diff_label_right.setStyleSheet('border-width: 2px;border-style: solid;' 
                                           'border-color: rgb(255, 170, 0);'
                                           'background-color:rgb(253, 245, 230);')



        # 布局放入bottom_widget中
        self.gridLayout_3.addWidget(self.left_label_2, 0, 0)
        self.gridLayout_3.addWidget(self.left_label_3, 0, 1)
        self.gridLayout_3.addWidget(self.diff_label_left, 1, 0)
        self.gridLayout_3.addWidget(self.diff_label_right, 1, 1)
        self.gridLayout_3.addWidget(self.TableWidget_left, 2, 0)
        self.gridLayout_3.addWidget(self.TableWidget_right, 2, 1)
        self.gridLayout_3.setSpacing(12)

        # self.TableWidget_left.itemSelectionChanged.co
        # 设置头部
        # self.TableWidget_left.setHorizontalHeaderLabels(self.diff_controller.get_left_table_head())
        # self.TableWidget_left.setHorizontalHeaderLabels(['111111', '2', '3333'])
        # self.TableWidget_right.setHorizontalHeaderLabels(self.diff_controller.get_right_table_head())
        # self.TableWidget_right.setHorizontalHeaderLabels(['111111', '2', '3333'])
        # 设置表格标题字体加粗
        font = self.TableWidget_left.horizontalHeader().font()
        font.setBold(True)
        self.TableWidget_left.horizontalHeader().setFont(font)
        self.TableWidget_right.horizontalHeader().setFont(font)
        # 设置表格为自适应的伸缩模式，即可根据窗口的大小来改变网格的大小
        # self.TableWidget_left.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        # 将表格设置为禁止编辑
        # self.TableWidget_left.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        # self.TableWidget_right.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        # 表格默认选择的是单个单元格，通过以下代码可以设置整行选中
        # TableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        # 将行与列的宽度高度与文本内容的宽高相匹配
        # QtWidgets.QTableWidget.resizeColumnsToContents(self.TableWidget_left)
        # QtWidgets.QTableWidget.resizeRowsToContents(self.TableWidget_left)

        self.TableWidget_left.clicked.connect(lambda: self.left_control_right())
        # self.TableWidget_left.cellClicked.connect(self.left_control_right)
        self.TableWidget_right.clicked.connect(lambda: self.right_control_left())
        # self.TableWidget_right.cellClicked.connect(self.right_control_left)

        self.bottom_group_box.setLayout(self.gridLayout_3)

    def deep_diff(self):
        if self.thread.is_on:
            self.insert_info("正在diff.........请稍后")
            return
        self.thread.start()
        self.thread.is_on = False
        self.insert_info("重新比对完成", 1, 1)

    def _deep_diff(self):
        self.rules[self.definition[0]][self.definition[5]] = self.text_1_2.text()
        self.rules[self.definition[1]][self.definition[5]] = self.text_2_2.text()
        self.rules[self.definition[2]][self.definition[5]] = self.text_3_2.text()
        if self.rules[self.definition[2]][self.definition[5]] != "":
            self.rules[self.definition[2]][self.definition[4]] = self.conbox_3_1.currentText()
        if self.rules[self.definition[1]][self.definition[5]] != "":
            self.rules[self.definition[1]][self.definition[4]] = self.conbox_2_1.currentText()
        if self.rules[self.definition[0]][self.definition[5]] != "":
            self.rules[self.definition[0]][self.definition[4]] = self.conbox_1_1.currentText()
        dif_array, dif_row_excel, dif_column_excel, dif_row_data, dif_column_data, data1, data2 = self.diff_controller.deep_diff(
            self.rules if not self.isReset else None, ret_new_data=True)
        return dif_array, dif_row_excel, dif_column_excel, dif_row_data, dif_column_data, data1, data2


    def set_diff_label_info(self, content1, content2):
        # print("c1: {}, c2: {}".format(content1, content2))
        self.diff_label_right.clear()
        self.diff_label_left.clear()
        if dif_data(content1, content2):
            self.diff_label_right.setText(
                BuildPackage.build_label_content(content2)
            )
            self.diff_label_left.setText(
                BuildPackage.build_label_content(content1)
            )
            return
        content1 = str(content1)
        content2 = str(content2)
        min_len = min(len(content1), len(content2))
        label_left = BuildPackage()
        label_right = BuildPackage()
        for i in range(min_len):
            if i % 60 == 0:
                label_left.insert('\n', is_diff=False)
                label_right.insert('\n', is_diff=False)
            if content1[i] != content2[i]:
                label_left.insert(content1[i], is_diff=True)
                label_right.insert(content2[i], is_diff=True)
            else:
                label_left.insert(content1[i], is_diff=False)
                label_right.insert(content2[i], is_diff=False)
        if min_len < len(content1):
            label_left = label_left.get_complete_package() + label_left.build_label_content(content1[min_len:], is_red=True)
            label_right = label_right.get_complete_package()
        else:
            label_left = label_left.get_complete_package()
            label_right = label_right.get_complete_package() + label_right.build_label_content(content2[min_len:], is_red=True)
        self.diff_label_right.setText(
            label_right
        )
        self.diff_label_left.setText(
           label_left
        )

    # 设置diff表格单元颜色
    def set_table_color(self, dif_array, row_data1, column_data1, row_data2, column_data2):
        self.next_index = -1
        self.diff_record = dif_array
        self.len_diff = len(dif_array)
        # print("diff_array: ", dif_array)
        if self.isReset:
            x_offset = 1
            y_offset = 0
        else:
            x_offset = 2
            y_offset = 1
        for x1, y1, x2, y2 in dif_array:
            if x1 == 1:
                continue
            # print("x1, y1, x2, y2, one, two:  ", x1, y1, x2, y2)
            # try:
            self.TableWidget_right.item(x1 - 2, y1 - 1 + y_offset).setForeground(
                QtGui.QBrush(QtGui.QColor(255, 0, 0)))
            self.TableWidget_right.item(x1 - 2, y1 - 1 + y_offset).setBackground(
                QtGui.QBrush(QtGui.QColor(255, 255, 0, 127)))
            self.TableWidget_left.item(x2 - 2, y2 - 1 + y_offset).setForeground(
                QtGui.QBrush(QtGui.QColor(255, 0, 0)))
            self.TableWidget_left.item(x2 - 2, y2 - 1 + y_offset).setBackground(
                QtGui.QBrush(QtGui.QColor(255, 255, 0, 127)))
            # except TypeError:


        # print("column_data1: ", column_data1)
        if column_data1:
            # for _y in range(len(content)):
            for x in range(column_data1[0], column_data1[1]):
                for _y in range(column_data1[3] - column_data1[2]):
                    self.TableWidget_left.item(x - x_offset, column_data1[2] + _y + y_offset).setBackground(
                        QtGui.QBrush(QtGui.QColor(255, 0, 0)))
        # print("column_data2: ", column_data2)

        if column_data2:
            # for _y in range(len(content)):
            for x in range(column_data2[0], column_data2[1]):
                for _y in range(column_data2[3] - column_data2[2]):
                    # print("x-x_offset: %s, y+_y+y_offset: %s" % (x-x_offset, y+_y+y_offset))
                    self.TableWidget_right.item(x - x_offset, column_data2[2] + _y + y_offset).setBackground(
                        QtGui.QBrush(QtGui.QColor(255, 0, 0)))
        # print("row_data1: ", row_data1)

        if x_offset == 1:
            if row_data1:
                # 第一个元素为-1时代表 表2无数据
                if len(row_data1) != 1:
                    for x in range(row_data1[0], row_data1[1]):
                        for y in range(row_data1[2]):
                            self.TableWidget_left.item(x - x_offset, y + y_offset).setBackground(
                                QtGui.QBrush(QtGui.QColor(255, 0, 0)))
            # print("row_data2: ", row_data2)
            if row_data2:
                for x in range(row_data2[0], row_data2[1]):
                    for y in range(row_data2[2]):
                        # print("x-offset, y", [x-x_offset, y])
                        self.TableWidget_right.item(x - x_offset, y + y_offset).setBackground(
                            QtGui.QBrush(QtGui.QColor(255, 0, 0)))
        else:
            # print("row_data1: ", row_data1)
            for x, content in row_data1:
                for y in range(len(content)):
                    self.TableWidget_left.item(x - x_offset, y + y_offset).setBackground(
                        QtGui.QBrush(QtGui.QColor(255, 0, 0)))
            # print("row_data2: ", row_data2)
            for x, content in row_data2:
                for y in range(len(content)):
                    # print("x-offset, y", [x-x_offset, y])
                    self.TableWidget_right.item(x - x_offset, y + y_offset).setBackground(
                        QtGui.QBrush(QtGui.QColor(255, 0, 0)))

    # 设置diff表格单元颜色
    def set_table_color_back(self, dif_array, row_data1, column_data1, row_data2, column_data2):
        # print("diff_array: ", dif_array)
        if self.isReset:
            x_offset = 1
            y_offset = 0
        else:
            x_offset = 2
            y_offset = 1
        for x1, y1, x2, y2, one, two in dif_array:
            if x1 == 1:
                continue
            # print("x1, y1, x2, y2, one, two:  ", x1, y1, x2, y2, one, two)
            self.TableWidget_right.item(x1-2, y1-1+y_offset).setForeground(QtGui.QBrush(QtGui.QColor(255, 0, 0)))
            # self.TableWidget_right.item(x1-2, y1-1+y_offset).setBackground(QtGui.QBrush(QtGui.QColor(0, 80, 0, 127)))
            self.TableWidget_right.item(x1-2, y1-1+y_offset).setBackground(QtGui.QBrush(QtGui.QColor(255, 255, 0, 127)))
            self.TableWidget_left.item(x2-2, y2-1+y_offset).setForeground(QtGui.QBrush(QtGui.QColor(255, 0, 0)))
            # self.TableWidget_left.item(x2-2, y2-1+y_offset).setBackground(QtGui.QBrush(QtGui.QColor(0, 80, 0, 127)))
            self.TableWidget_left.item(x2-2, y2-1+y_offset).setBackground(QtGui.QBrush(QtGui.QColor(255, 255, 0, 127)))

        # print("column_data1: ", column_data1)
        for x, y, content in column_data1:
            # for _y in range(len(content)):
            for _y in range(content-y):
                self.TableWidget_left.item(x-x_offset, y+_y+y_offset).setBackground(QtGui.QBrush(QtGui.QColor(255, 0, 0)))
        # print("column_data2: ", column_data2)
        for x, y, content in column_data2:
            # for _y in range(len(content)):
            for _y in range(content-y):
                # print("x-x_offset: %s, y+_y+y_offset: %s" % (x-x_offset, y+_y+y_offset))
                self.TableWidget_right.item(x-x_offset, y+_y+y_offset).setBackground(QtGui.QBrush(QtGui.QColor(255, 0, 0)))
        # print("row_data1: ", row_data1)
        for x, content in row_data1:
            for y in range(len(content)):
                self.TableWidget_left.item(x-x_offset, y+y_offset).setBackground(QtGui.QBrush(QtGui.QColor(255, 0, 0)))
        # print("row_data2: ", row_data2)
        for x, content in row_data2:
            for y in range(len(content)):
                # print("x-offset, y", [x-x_offset, y])
                self.TableWidget_right.item(x-x_offset, y+y_offset).setBackground(QtGui.QBrush(QtGui.QColor(255, 0, 0)))




    # 刷新表格数据
    def inset_data(self, data1, data2, data1_header, data2_header):
        self.TableWidget_left.clear()
        self.TableWidget_right.clear()
        max_width = max(len(data1_header), len(data2_header))
        max_heigth = max(len(data1), len(data2))
        self.TableWidget_left.setRowCount(max_heigth)
        self.TableWidget_left.setColumnCount(max_width)
        self.TableWidget_right.setRowCount(max_heigth)
        self.TableWidget_right.setColumnCount(max_width)
        # print("data1_header: ", data1_header)
        # print("data2_header: ", data2_header)

        self.TableWidget_left.setHorizontalHeaderLabels(data1_header or [])
        self.TableWidget_right.setHorizontalHeaderLabels(data2_header or [])
        for i in range(len(data1)):
            for j in range(len(data1[i])):
                value = str(data1[i][j])
                if value.endswith(".0"):
                    value = value[:-2]
                self.TableWidget_left.setItem(
                    i,
                    j,
                    QtWidgets.QTableWidgetItem(value)
                )
        for i in range(len(data2)):
            for j in range(len(data2[i])):
                value = str(data2[i][j])
                if value.endswith(".0"):
                    value = value[:-2]
                self.TableWidget_right.setItem(
                    i,
                    j,
                    QtWidgets.QTableWidgetItem(value)
                )

    def reset_button(self):
        # print("self.rules: ", self.rules)
        # print("888888888888: ", self.rules[self.definition[0]][self.definition[3]] or '筛选条件')

        self.conbox_1.setCurrentText(
            self.rules[self.definition[0]][self.definition[3]] or '筛选条件'
        )
        self.conbox_2.setCurrentText(
            self.rules[self.definition[1]][self.definition[3]] or '筛选条件'
        )

        self.conbox_3.setCurrentText(
            self.rules[self.definition[2]][self.definition[3]] or '筛选条件'
        )

        self.conbox_1_1.setCurrentText(
            self.rules[self.definition[0]][self.definition[4]] or '>'
        )
        self.conbox_2_1.setCurrentText(
            self.rules[self.definition[1]][self.definition[4]] or '>'
        )

        self.conbox_3_1.setCurrentText(
            self.rules[self.definition[2]][self.definition[4]] or '>'
        )

        self.text_1_2.setText(
            self.rules[self.definition[0]][self.definition[5]]
        )

        self.text_2_2.setText(
            self.rules[self.definition[1]][self.definition[5]]
        )

        self.text_3_2.setText(
            self.rules[self.definition[2]][self.definition[5]]
        )

        self.top_left_combox.setCurrentText(
            self.rules[self.definition[6]] or '筛选条件'

        )


    def create_top_central_group_box(self):
        self.top_central_group_box = QtWidgets.QGroupBox("比对条件（可选）：")
        self.gridLayout_1 = QtWidgets.QGridLayout()
        self.conbox_1 = QtWidgets.QComboBox()
        # print("self.names: ", self.names)
        self.conbox_1.addItems(["筛选条件"] + self.names)
        self.conbox_1.currentIndexChanged.connect(
            lambda *args: self.choose_key(self.conbox_1, self.definition[0], self.definition[3]))
        # self.conbox_1.addItems(['11', '12', '13'])
        self.conbox_2 = QtWidgets.QComboBox()
        self.conbox_2.addItems(["筛选条件"] + self.names)
        self.conbox_2.currentIndexChanged.connect(
            lambda *args: self.choose_key(self.conbox_2, self.definition[1], self.definition[3]))
        # self.conbox_2.addItems(['21', '22', '23'])
        self.conbox_3 = QtWidgets.QComboBox()
        self.conbox_3.addItems(["筛选条件"] + self.names)
        self.conbox_3.currentIndexChanged.connect(
            lambda *args: self.choose_key(self.conbox_3, self.definition[2], self.definition[3]))
        # self.conbox_3.addItems(['31', '32', '33'])
        self.conbox_1_1 = QtWidgets.QComboBox()
        self.conbox_1_1.addItems(self.relation)
        self.conbox_1_1.currentIndexChanged.connect(
            lambda *args: self.choose_key(self.conbox_1_1, self.definition[0], self.definition[4]))
        # self.conbox_1_1.addItems(['11', '12', '13'])
        self.conbox_2_1 = QtWidgets.QComboBox()
        self.conbox_2_1.addItems(self.relation)
        self.conbox_2_1.currentIndexChanged.connect(
            lambda *args: self.choose_key(self.conbox_2_1, self.definition[1], self.definition[4]))
        # self.conbox_2_1.addItems(['21', '22', '23'])
        self.conbox_3_1 = QtWidgets.QComboBox()
        self.conbox_3_1.addItems(self.relation)
        self.conbox_3_1.currentIndexChanged.connect(
            lambda *args: self.choose_key(self.conbox_3_1, self.definition[2], self.definition[4]))
        # self.conbox_3_1.addItems(['31', '32', '33'])
        self.text_1_2 = QtWidgets.QLineEdit()
        self.text_1_2.textChanged.connect(
            lambda *args: self.choose_label(self.text_1_2, self.definition[0], self.definition[5]))
        self.text_2_2 = QtWidgets.QLineEdit()
        self.text_2_2.textChanged.connect(
            lambda *args: self.choose_label(self.text_2_2, self.definition[1], self.definition[5]))
        self.text_3_2 = QtWidgets.QLineEdit()
        self.text_3_2.textChanged.connect(
            lambda *args: self.choose_label(self.text_3_2, self.definition[2], self.definition[5]))
        self.text_1_2.setMaximumSize(120, 30)
        self.text_2_2.setMaximumSize(120, 30)
        self.text_3_2.setMaximumSize(120, 30)

        self.gridLayout_1.addWidget(self.conbox_1, 1, 5)
        self.gridLayout_1.addWidget(self.conbox_2, 2, 5)
        self.gridLayout_1.addWidget(self.conbox_3, 3, 5)
        self.gridLayout_1.addWidget(self.conbox_1_1, 1, 6)
        self.gridLayout_1.addWidget(self.conbox_2_1, 2, 6)
        self.gridLayout_1.addWidget(self.conbox_3_1, 3, 6)
        self.gridLayout_1.addWidget(self.text_1_2, 1, 7)
        self.gridLayout_1.addWidget(self.text_2_2, 2, 7)
        self.gridLayout_1.addWidget(self.text_3_2, 3, 7)

        self.top_central_group_box.setLayout(self.gridLayout_1)
        self.top_central_group_box.setMaximumSize(320, 160)

    def choose_key(self, com, index, key):
        if index == 0:
            # print("key: ", key)
            self.rules[key] = com.currentText()
            self.insert_info('(%s)选择成功： %s' % (key, self.rules[key]), 1)
        else:
            # print("index: %s, key: %s" % (index, key))
            self.rules[index][key] = com.currentText()
            self.insert_info('(%s)选择(%s)成功： %s' % (str(index), str(key), self.rules[index][key]), 1)
        if self.isReset:
            self.isReset = False

    def choose_label(self, com, index, key):
        self.rules[index][key] = com.text()
        self.insert_info('(%s)选择(%s)成功： %s' % (index, key, self.rules[index][key]), 1)
        if self.isReset:
            self.isReset = False


    def left_control_right(self):
        index = self.TableWidget_left.currentIndex()
        # print(index)
        # 同步右表视角
        self.TableWidget_right.setCurrentCell(
            index.row(),
            index.column()
        )
        # 切换光标到右表
        self.TableWidget_right.setFocus()
        item_left = self.TableWidget_left.currentItem()
        item_right = self.TableWidget_right.currentItem()

        self.set_diff_label_info(
            item_left.text() if item_left else "",
            item_right.text() if item_right else "",
        )

    def right_control_left(self):
        index = self.TableWidget_right.currentIndex()
        # print(index)
        # 同步左表视角
        self.TableWidget_left.setCurrentCell(
            index.row(),
            index.column()
        )
        # 切换光标到左表
        self.TableWidget_left.setFocus()
        item_left = self.TableWidget_left.currentItem()
        item_right = self.TableWidget_right.currentItem()

        self.set_diff_label_info(
            item_left.text() if item_left else "",
            item_right.text() if item_right else "",
        )


    # 控制窗口显示在屏幕中心的方法
    def center(self):
        # 获得窗口
        qr = self.father.frameGeometry()
        # 获得屏幕中心点
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        # 显示到屏幕中心
        qr.moveCenter(cp)
        self.father.move(qr.topLeft())

if __name__ == '__main__':
    # from page.function import Fun
    # app = QtWidgets.QApplication(sys.argv)
    # father = QtWidgets.QMainWindow()
    # win=Table('111111111', None, [[str(i) for i in range(5)], [str(i) for i in range(5)]],
    #           Fun(
    #               [[str(i) for i in range(5)],[str(i) for i in range(5)]],
    #               [[str(i) for i in range(5)],[str(i) for i in range(5)]],
    #               [[str(i) for i in range(5)], [str(i) for i in range(5)]],
    #               father
    #           )
    #           )
    # win.set_table_color([[2, 2, 2, 2, 0, 0]], [], [], [], [])
    # # win.inset_data()
    # # father.show()
    # sys.exit(app.exec_())

    content1 = "集齐90张穆萨·西索科签约信可与白鹿巷穆萨·西索科进行签约"
    content2 = "集齐90张本·戴维斯签约信可与白鹿巷本·戴维斯进行签约"
    min_len = min(len(content1), len(content2))
    label_left = BuildPackage()
    label_right = BuildPackage()
    for i in range(min_len):
        if content1[i] != content2[i]:
            label_left.insert(content1[i], is_diff=True)
            label_right.insert(content2[i], is_diff=True)
        else:
            label_left.insert(content1[i], is_diff=False)
            label_right.insert(content2[i], is_diff=False)
    if min_len < len(content1):
        label_left = label_left.get_complete_package() + label_left.build_label_content(content1[min_len:], is_red=True)
        label_right = label_right.get_complete_package()
    else:
        label_left = label_left.get_complete_package()
        label_right = label_right.get_complete_package() + label_right.build_label_content(content2[min_len:],
                                                                                           is_red=True)


