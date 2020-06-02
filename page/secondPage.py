# -*- coding: utf-8 -*-
# @Time    : 2019/11/25 17:23
# @Author  : zzt
# @File    : secondPage.py

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os
from tkinter import messagebox
import datetime
from Util import linkdatabase, dataanalyze
import sys
from page.function import show_dif, show_dif_ui, check_datas
import configparser
from Util.download_data import HttpClient
from Util.mailUtil import MailClient
from Util.login.factory_client import FactoryHttpClient
import time
from Util.uiShow import pb2dict, except_ui_show


#存放服务器信息
servers = dict()

#servers['篮球242'] = "192.168.1.242", "root", "wckj#2017", 3306
#servers['篮球242_1(内网)'] = "192.168.1.242", "nbatest", "DGAG(&Jh23858klh", 3306
servers['篮球201(内网)'] = "192.168.1.201", "test", "L*&k34HC98K.kDG%KH", 3307
servers['篮球139_合服(内网)'] = "192.168.1.139", "lizheng", "DT*^^kjdg245", 3306
servers['新足球(内网)'] = "192.168.1.201", "root", "KH*^35KH@%%9654", 3309
servers['新足球(外网)'] = "47.94.228.86", "test", "S7#ks%^&&*khlls234", 3306
servers['老足球(内网)'] = "192.168.1.204", "root", "wckj#2015", 3306
servers['老足球(内网126)'] = "192.168.1.126", "root", "wckj@2018", 3306
servers['中超(内网)'] = "192.168.1.204", "root", "wckj#2015", 3306
#存放活跃数据库对象实例useserver['now'] = xxx
useserver = dict()
managemnt_background = ["篮球国内", "篮球港澳台", "最佳11人"]

def get_now_time():
    return datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')

class SecondPage():

    def __init__(self, parent):
        self.parent = parent
        self._account = ['', '', '', '', ''] #存放管理后台账号 邮箱账号
        self.create_buttons()
        #self.init_account()
        self._http = None
        self.server_list = {}
        self.server_id = None

    def create_buttons(self):
        tapcontrol = ttk.Notebook(self.parent, height=70, width=796)
        tab1 = tk.Frame(tapcontrol)
        tapcontrol.add(tab1, text='内网母-库比对')
        tab2 = tk.Frame(tapcontrol)
        tapcontrol.add(tab2, text='内网新-老库比对')
        tab3 = tk.Frame(tapcontrol)
        tapcontrol.add(tab3, text='版本数据表差异')
        tab4 = tk.Frame(tapcontrol)
        tapcontrol.add(tab4, text='线上母-库比对')
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

        #第二页四小页
        but5_4 = tk.Button(tab4, text='登录账号', command=lambda: self.set_account(), width=15)
        but5_4.grid(row=0, column=0, padx=5, pady=3, rowspan=2)
        # but0_4 = tk.Button(tab4, text='一键登录后台和邮件', command=lambda: self.select_server(), width=18)
        # but0_4.grid(row=0, column=1, padx=5, pady=3, rowspan=2)
        self.com1_4 = ttk.Combobox(tab4, state='readonly')
        self.com1_4.bind("<<ComboboxSelected>>", lambda *args: self.show_server(self.com1_4))
        self.com1_4.set('选择服务器')
        self.com1_4.grid(row=0, column=2, padx=10, pady=3)
        # 添加选择数据库下拉按钮
        self.com2_4 = ttk.Combobox(tab4, state='readonly')
        self.com2_4.bind("<<ComboboxSelected>>", lambda *args: self.show_database(self.com1_4, self.com2_4))
        self.com2_4.set('选择数据库')
        self.com2_4.grid(row=1, column=2, padx=10, pady=3)
        # 添加文本显示框
        ent1_v_4 = tk.StringVar()
        ent1_4 = tk.Entry(tab4, textvariable=ent1_v_4, width=23)
        ent1_v_4.set('导入配置文件')
        ent1_4.grid(row=0, column=3, padx=3, pady=1)
        ent2_v_4 = tk.StringVar()
        ent2_4 = tk.Entry(tab4, textvariable=ent2_v_4, width=23)
        ent2_v_4.set('导入母文件')
        ent2_4.grid(row=1, column=3, padx=3, pady=1)
        # 添加导入文件按钮
        but1_4 = tk.Button(tab4, text='导入', command=lambda: self.import_file(ent1_v_4, tex, True))
        but1_4.grid(row=0, column=4, padx=3, pady=1)
        but2_4 = tk.Button(tab4, text='导入', command=lambda: self.import_file(ent2_v_4, tex, False))
        but2_4.grid(row=1, column=4, padx=3, pady=1)
        # 添加保存母文件按钮
        ent3_v_4 = tk.StringVar()
        ent3_4 = tk.Entry(tab4, textvariable=ent3_v_4, width=12)
        ent3_4.grid(row=0, column=5, padx=3, pady=1)
        ent3_v_4.set('自定义文件名')
        but3_4 = tk.Button(tab4, text='保存母文件', command=lambda: self.save_file_4(ent1_v_4, ent3_v_4), width=12)
        but3_4.grid(row=0, column=6, padx=3, pady=1)
        but4_4 = tk.Button(tab4, text='开始检查', command=lambda: self.button_check_file_4(ent2_v_4, tex), width=26)
        but4_4.grid(row=1, column=5, padx=3, pady=1, columnspan=2)



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
        but8 = tk.Button(self.parent, text='下一个', command=lambda: self.next_cursor())
        but8.pack(anchor=tk.S, side=tk.RIGHT, padx=3, pady=5)
        self.tex = tex
        self.tex.tag_config('tag1', foreground='green')
        self.tex.tag_config('tag2', foreground='red')

    def next_cursor(self):
        pos = self.tex.search("存在差异", tk.INSERT)
        if not pos:
            self.insert_info("未找到目标内容", 1)
        else:
            x, y = pos.split('.')
            self.tex.mark_set("insert", ".".join([x, str(int(y)+4)]))
            self.tex.see(pos)

    def set_account(self):
        self.reset_account()
        top = tk.Toplevel()
        top.title("管理账号密码")
        #设置窗口初始位置
        top.geometry("+800+400")
        tk.Label(top, text="选择服务器：").grid(row=0, column=0, padx=3, pady=1)
        com = ttk.Combobox(top, state='readonly')
        com.bind("<<ComboboxSelected>>", lambda *args: self.load_account(ent6_v_1, ent6_v_2, ent6_v_3, ent6_v_4, com))
        com.set('下拉选择服务器')
        com['values'] = managemnt_background
        com.grid(row=0, column=1, padx=10, pady=3)
        tk.Label(top, text="管理后台账号：").grid(row=1, column=0, padx=3, pady=1)
        tk.Label(top, text="管理后台密码：").grid(row=2, column=0, padx=3, pady=1)
        tk.Label(top, text="验证的邮箱账号：").grid(row=3, column=0, padx=3, pady=1)
        tk.Label(top, text="验证的邮箱密码：").grid(row=4, column=0, padx=3, pady=1)
        ent6_v_1 = tk.StringVar()
        ent6_1 = tk.Entry(top, textvariable=ent6_v_1, width=26)
        ent6_1.grid(row=1, column=1, padx=3, pady=1)
        ent6_v_2 = tk.StringVar()
        ent6_2 = tk.Entry(top, textvariable=ent6_v_2, width=26)
        ent6_2.grid(row=2, column=1, padx=3, pady=1)
        ent6_v_3 = tk.StringVar()
        ent6_3 = tk.Entry(top, textvariable=ent6_v_3, width=26)
        ent6_3.grid(row=3, column=1, padx=3, pady=1)
        ent6_v_4 = tk.StringVar()
        ent6_4 = tk.Entry(top, textvariable=ent6_v_4, width=26)
        ent6_4.grid(row=4, column=1, padx=3, pady=1)
        but6_1 = tk.Button(top, text='保存账号', command=lambda: self.save_account(ent6_v_1, ent6_v_2, ent6_v_3, ent6_v_4, com), width=12)
        but6_1.grid(row=1, column=2, padx=3, pady=1, rowspan=2)
        but6_1 = tk.Button(top, text='登录账号', command=lambda: self.login(), width=12)
        but6_1.grid(row=3, column=2, padx=3, pady=1, rowspan=2)
        #self.load_account(ent6_v_1, ent6_v_2, ent6_v_3, ent6_v_4)

    def save_account(self, ent0, ent1, ent2, ent3, com):
        self._account[0] = com.get()
        if self._account[0] not in managemnt_background:
            self.insert_info("保存失败！ 没有选择服务器", 1, 2)
            self._account[0] = ''
            return
        self._account[1] = ent0.get()
        _content = ent1.get()
        if _content != "******":
            self._account[2] = ent1.get()
        self._account[3] = ent2.get()
        _content = ent3.get()
        if _content != "******":
            self._account[4] = ent3.get()

        if '' in self._account:
            self.insert_info("保存失败！ 请检查账号信息是否填写完整", 1, 2)
            return
        cfg = configparser.ConfigParser()
        cfg.read('cfg.ini')

        cfg[self._account[0]] = {}
        cfg[self._account[0]]['服务器'] = self._account[0]
        cfg[self._account[0]]['管理后台账号'] = self._account[1]
        cfg[self._account[0]]['管理后台密码'] = self._account[2]
        cfg[self._account[0]]['验证的邮箱账号'] = self._account[3]
        cfg[self._account[0]]['验证的邮箱密码'] = self._account[4]
        with open('cfg.ini', 'w') as f:
            cfg.write(f)

        self.insert_info('服务器： %s' % self._account[0], 1, 1)
        self.insert_info('管理后台账号： %s' % self._account[1], 1, 1)
        self.insert_info('管理后台密码： ******', 1, 1)
        self.insert_info('验证的邮箱账号： %s' % self._account[3], 1, 1)
        self.insert_info('验证的邮箱密码： ******', 1, 1)
        self.insert_info('保存成功！', 1, 1)

    def load_account(self, ent0, ent1, ent2, ent3, com):
        cfg = configparser.ConfigParser()
        cfg.read('cfg.ini')
        style = com.get()
        if style in cfg.sections():
            self._account[0] = style
            self._account[1] = cfg[style]['管理后台账号']
            self._account[2] = cfg[style]['管理后台密码']
            self._account[3] = cfg[style]['验证的邮箱账号']
            self._account[4] = cfg[style]['验证的邮箱密码']
            ent0.set(self._account[1])
            ent1.set("******")
            ent2.set(self._account[3])
            ent3.set("******")
            self.insert_info('读取管理后台/邮箱账号成功！', 1, 1)
        else:
            ent0.set('')
            ent1.set('')
            ent2.set('')
            ent3.set('')
            self.insert_info('读取管理后台/邮箱账号失败 ：%s' % style, 1, 2)

    def init_account(self):
        cfg = configparser.ConfigParser()
        cfg.read('cfg.ini')
        section_list = cfg.sections()
        if section_list == [] or 'account' not in section_list:
            self.insert_info('配置文件《config.ini》不存在或没有管理后台/邮箱账号信息! 请先修改后台和邮件信息', 1)
        else:
            self._account[0] = cfg['account']['服务器']
            self._account[1] = cfg['account']['管理后台账号']
            self._account[2] = cfg['account']['管理后台密码']
            self._account[3] = cfg['account']['验证的邮箱账号']
            self._account[4] = cfg['account']['验证的邮箱密码']
            self.insert_info('读取管理后台/邮箱账号成功！ 可一键登录后台和邮件', 1, 1)

    def select_server(self):
        pass

    def reset_account(self):
        self._account = ['', '', '', '', '']

    #@except_ui_show
    def login(self):
        if '' in self._account:
            self.insert_info('请先填写管理后台账号!', 1, 2)
            return
        if self._account[0] not in managemnt_background:
            self.insert_info('登陆管理后台失败，服务器选择错误！ ： %s' % str(self._account), 1, 2)
            return
        #初始化http
        self._http = FactoryHttpClient().create_client(self._account[0], self)
        ret = self._http.login(self._account[1:])
        print(str(ret))
        # #先登录
        # self.insert_info('正在登陆管理后台账号：%s ...' % self._account[1], 1)
        # self._http.login(self._account[1], self._account[2])
        # self.insert_info('登陆管理后台账号成功。-》下一步登录邮箱', 1, 1)
        # #time.sleep(1)
        # #a = MailClient('liyang@galasports.net', "23fPa'62")
        # #登录邮箱
        # self.insert_info('正在登陆验证码邮件账号：%s...' % self._account[3], 1)
        # a = MailClient(self._account[3], self._account[4])
        # self.insert_info('登陆验证码邮件账号成。 -》下一步验证邮箱', 1, 1)
        # #获取验证码
        # msg = a.find_my_mail('account@galasports.com', 'The server authentication code-GALA Sports').split(':')[1][:4]
        # self.insert_info('获取邮箱验证码《%s》成功. —》下一步验证....' % msg, 1,)
        # a.close()
        # #发送验证码
        # ret = self._http.verification_email(msg)
        # if ret.ret != 0:
        #     self.insert_info("验证失败： %s" % ret.msg)
        #     return
        # ret = pb2dict(ret)
        # import json
        # ret = json.loads(pb2json(ret))
        #解析回包内容初始化UI中的下拉框
        self.server_list = {}
        if self._account[0] == managemnt_background[0]:
            self.server_list["data库"] = self.list2dict(ret["date_jdbc"])
            self.server_list["选服"] = self.list2dict(ret["sel_jdbc"])
            self.server_list["提审服"] = self.list2dict(ret["jdbc_info"], "STS")
            self.server_list["官网"] = self.list2dict(ret["jdbc_info"], "SLI")
            self.server_list["混服"] = self.list2dict(ret["jdbc_info"], "SLY")
            self.server_list["腾讯"] = self.list2dict(ret["jdbc_info"], "STX")
            self.com1_4['values'] = list(self.server_list.keys())
            self.insert_info('邮箱验证成功， 所有步骤操作完成！！！', 1, 1)
        elif self._account[0] == managemnt_background[1]:
            self.server_list["data库"] = self.list2dict(ret["date_jdbc"])
            self.server_list["选服"] = self.list2dict(ret["sel_jdbc"])
            self.server_list["港澳台"] = self.list2dict(ret["jdbc_info"], "SSEA")
            self.com1_4['values'] = list(self.server_list.keys())
            self.insert_info('邮箱验证成功， 所有步骤操作完成！！！', 1, 1)
        elif self._account[0] == managemnt_background[2]:
            self.server_list["data库"] = self.list2dict(ret["date_jdbc"])
            self.server_list["官网"] = self.list2dict(ret["game_jdbc"], "SIOS")
            self.server_list["混服"] = self.list2dict(ret["game_jdbc"], "SLY")
            self.server_list["腾讯"] = self.list2dict(ret["game_jdbc"], "STX")
            self.com1_4['values'] = list(self.server_list.keys())
            self.insert_info('服务器信息拉取成功， 所有步骤操作完成！！！', 1, 1)


    def list2dict(self, obj, key=''):
        if isinstance(obj, dict):
            obj = [obj]
        _dict = {}
        for i in obj:
            if i["server_id"].startswith(key):
                _dict.update({i["server_name"]: i["server_id"]})
        return _dict

    def show_server(self, com):
        _key = com.get()
        self.com2_4['values'] = list(self.server_list[_key])
        self.insert_info('选择的服务器名为： %s' % _key, 1)

    def show_database(self, com1, com2):
        _key = com2.get()
        self.server_id = self.server_list[com1.get()][_key]
        self.insert_info('选择的数据库名为： %s' % _key, 1)


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
        if ld == None:
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

    # def generally_import_file(self, v, tex, is_save):
    #     path = filedialog.askopenfilename(filetypes=[('XLSX', '.xlsx'), ('XLS', '.xls')])
    #     if path == '':
    #         now_time = self.get_now_time()
    #         tex.insert(tk.END, now_time+': 没有选中导入文件\n')
    #         return
    #     v.set(path)
    #     array = dataanalyze.read_excel_sheets(path)
    #     if "字段表" in array:
    #         pass
    #         #todo 读取字段类型未实现
    #     else:
    #         if is_save:
    #             array = dataanalyze.read_save_names(path)
    #         else:
    #             array = dataanalyze.read_excel_names(path)
    #     if array == -1:
    #         now_time = self.get_now_time()
    #         tex.insert(tk.END, now_time+': 文件第一页内容为空或超过500行/列，请检查配置文件\n')
    #         return
    #     elif array == -2:
    #         now_time = self.get_now_time()
    #         tex.insert(tk.END, now_time+': 文件页签不应该包含‘sheet’或其他错误，请检查母文件\n')
    #         return
    #     if not is_save:
    #         array = array.keys()
    #     for name in array:
    #         try:
    #             tex.insert(tk.END, name+'\n')
    #         except:
    #             error_buf = sys.exc_info()
    #             messagebox.showerror(error_buf[0].__name__, error_buf[1])




    def import_file(self, v, tex, is_save):
        path = filedialog.askopenfilename(filetypes=[('XLSX', '.xlsx'), ('XLS', '.xls')])
        if path == '':
            now_time = self.get_now_time()
            tex.insert(tk.END, now_time+': 没有选中导入文件\n')
            return
        v.set(path)
        if is_save:
            array = dataanalyze.read_save_names(path)
            print("array:", str(array))
        else:
            array = dataanalyze.read_excel_names(path)
        if array == -1:
            now_time = self.get_now_time()
            tex.insert(tk.END, now_time+': 文件第一页内容为空或超过500行/列，请检查配置文件\n')
            return
        elif array == -2:
            now_time = self.get_now_time()
            tex.insert(tk.END, now_time+': 文件页签不应该包含‘sheet’或其他错误，请检查母文件\n')
            return
        if not is_save:
            array = array.keys()
        for name in array:
            try:
                tex.insert(tk.END, str(name)+'\n')
            except:
                error_buf = sys.exc_info()
                messagebox.showerror(error_buf[0].__name__, error_buf[1])

    def is_field_table(self, tables):
        #判断是否为字段下载方式
        for name in ['tables', "key", "value"]:
            if name not in tables:
                return False
        return True

    def save_file_4(self, v, v1):
        #保存配置表可能需要一些时间这里应考虑锁屏
        path = v.get()
        if not os.path.isfile(path):
            self.insert_info('没有选择配置表或者文件路径不正确， 请检查', 1, 2)
            return
        if self.server_id == None:
            self.insert_info('没有选择服务器', 1, 2)
            return
        local_table_names = dataanalyze.read_save_names(path)
        if local_table_names == -1:
            self.insert_info('文件第一页内容为空或超过300行/列，请检查配置文件', 1, 2)
            return
        field_tables = ''
        if self._account[0] == managemnt_background[2]:
            #最佳11人
            params = []
            if not self.is_field_table(local_table_names):
                #正常下载方式
                params = [{'table_name': table_name} for table_name in local_table_names]
                query_type = 1
            else:
                #字段表下载方式
                query_type = 2
                #params = [{'table_name': "t_team", "col_name": "team_id", "col_value": ["111mb", "1114a"]}]
                field_tables = dataanalyze.read_field_table(path)
                if field_tables == -1:
                    self.insert_info("字段下载文件没有内容或不是 tables， key， value 格式", 1, 2)
                    return
                print("field_tables: ", str(field_tables))
                for item in field_tables:
                    _col_value = list(map(lambda x: x if not isinstance(x, float) else str(int(x)), item['col_value']))
                    for _ in item.get('table_name', []):
                        params.append({"table_name": _, "col_name": item['col_name'][0], "col_value": _col_value})
            data = {
                "server_id": self.server_id,
                "source_mark": "data" if "data" in self.com1_4.get() else "game",
                #"source_mark": "game",
                "query_type": query_type,
                "query_param": params,
            }
        else:
            #篮球
            data = {
                "server_id": self.server_id,
                "table_name": local_table_names
            }
        print("data:", str(data))
        ret = self._http.download_content(data)
        if self._account[0] == managemnt_background[2]:
            if getattr(ret, "ret"):
                self.insert_info("下载数据失败： %s" % ret.extra, 1, 2)
                return
            print("ret = ", str(ret))
        else:
            if ret.ret != 0:
                self.insert_info("下载数据失败： %s" % ret.res, 1, 2)
                return
        data = pb2dict(ret)
        remote_data = dict()
        for _ in data['data']:
            remote_data[_['table_name']] = _['data']
        bigdatas = dict()
        remote_table_names = list(remote_data.keys())
        if self.is_field_table(local_table_names):
            local_table_names = []
            #为字段下载表添加field内容用于比对时收集目标表
            remote_data['field'] = field_tables
            for item in field_tables:
                local_table_names.extend(item.get('table_name'))

        if len(set(local_table_names)) != len(remote_table_names):
            self.insert_info("下载的数据表数量与导入配置表不一致，请联系管理员", 1, 2)
            self.insert_info("下载的数据表: %s " % remote_table_names, 1)
            self.insert_info("导入的配置表: %s " % local_table_names, 1)
            return
        for _key, _value in remote_data.items():
            content = []
            if _key != "field":
                for _ in _value:
                    content.append(_.split('|'))
            else:
                content = _value
            bigdatas[_key] = content
        if not os.path.exists('配置文件夹'):
            os.mkdir('配置文件夹')
        if not os.path.exists('配置文件夹\母文件'):
            os.mkdir('配置文件夹\母文件')
        filename = v1.get()+'_'
        if filename == '自定义文件名_':
            filename = ''
        filename = ''.join([os.getcwd(), '\配置文件夹\母文件\\', filename, '母文件_', get_now_time().replace(':', '_'), '.xlsx'])
        key = dataanalyze.write_excel(bigdatas, filename)
        if key:
            self.insert_info('保存成功, 路径为<%s>' % filename, 1, 1)
        else:
            self.insert_info('没东西可保存或表名超过50个字符', 1, 2)

    def save_file(self, v, v1, tex):
        #保存配置表可能需要一些时间这里应考虑锁屏
        path = v.get()
        if not os.path.isfile(path):
            now_time = self.get_now_time()
            tex.insert(tk.END, now_time+': 没有选择配置表或者文件路径不正确， 请检查\n')
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
            tex.insert(tk.END, now_time+': 文件第一页内容为空或超过500行/列，请检查配置文件\n')
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
            if len(datas) == 0:
                datas = useserver['now'].get_table_row([name])
                datas = [dataanalyze.change_dic(datas)[1:]]
                #print("name = %s , datas = %s " % (name, str(datas)))
            else:
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
    def is_valid_4(self, path):
        if not os.path.isfile(path):
            self.insert_info('没有选择配置表或者文件路径不正确， 请检查', 1, 2)
            return False

        if self.server_id == None:
            self.insert_info('没有选择服务器', 1, 2)
            return False

        names = dataanalyze.read_excel_names(path)
        if names == -2:
            self.insert_info('文件页签不应该包含‘sheet’或其他错误，请检查母文件', 1, 2)
            return False

        if len(names) >= 1000:
            self.insert_info('需要检查的表数量太多， 超过1000个。 操作失败', 1, 2)
            return False

        return True

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
            tex.search()
            return False
        names = dataanalyze.read_excel_names(path)
        if names == -2:
            now_time = self.get_now_time()
            tex.insert(tk.END, now_time + ': 文件页签不应该包含‘sheet’或其他错误，请检查母文件\n')
            return False
        if len(names) >= 1000:
            now_time = self.get_now_time()
            tex.insert(tk.END, now_time + ': 需要检查的表数量太多， 超过1000个。 操作失败\n')
            return False
        return True


    #用于检查配置表与数据库表的差异
    def button_check_file_4(self, v, tex):
        path = v.get()
        if not self.is_valid_4(path):
            return
        #time_6 = time.clock()
        local_datas = dataanalyze.read_excel_mu_datas(path)
        # print('一次性读取所有数据花费时间： %f'%(time.clock()-time_6))
        local_table_names = list(local_datas.keys())
        if self._account[0] == managemnt_background[2]:
            #最佳11人
            #todo 还需具体实现
            params = []
            if "field" not in local_table_names:
                #正常下载方式
                params = [{'table_name': table_name} for table_name in local_table_names]
                query_type = 1
            else:
                # 字段表下载方式
                query_type = 2
                # params = [{'table_name': "t_team", "col_name": "team_id", "col_value": ["111mb", "1114a"]}]
                field_tables = dataanalyze.read_field_table(path)
                if field_tables == -1:
                    self.insert_info("字段下载文件没有内容或不是 tables， key， value 格式", 1, 2)
                    return
                print("field_tables: ", str(field_tables))
                for item in field_tables:
                    _col_value = list(map(lambda x: x if not isinstance(x, float) else str(int(x)), item['col_value']))
                    for _ in item.get('table_name', []):
                        params.append({"table_name": _, "col_name": item['col_name'][0], "col_value": _col_value})

            data = {
                "server_id": self.server_id,
                "source_mark": "data" if "data" in self.com1_4.get() else "game",
                "query_type": query_type,
                "query_param": params,
            }
        else:
            #篮球
            data = {
                "server_id": self.server_id,
                "table_name": local_table_names
            }
        ret = self._http.download_content(data)
        if ret.ret != 0:
            self.insert_info("下载数据失败： %s" % ret.res, 1, 2)
            return
        data = pb2dict(ret)
        bigdatas = dict()
        for _ in data['data']:
            bigdatas[_['table_name']] = _['data']
        del data
        #存放数据库所有数据
        remote_datas = dict()
        # 存放数据库所有表名
        remote_table_names = list(bigdatas.keys())
        if "field" in local_table_names:
            local_table_names.remove('field')
        if len(local_table_names) != len(remote_table_names):
            self.insert_info("下载的数据表数量与导入配置表不一致，请联系管理员", 1, 2)
            self.insert_info("下载的数据表: %s " % remote_table_names, 1)
            self.insert_info("导入的配置表: %s " % local_table_names, 1)
            return
        for _key, _value in bigdatas.items():
            content = []
            for _ in _value:
                content.append(_.split('|'))
            remote_datas[_key] = content
        del bigdatas

        #index = 1
        for name in local_table_names:
            data_array = remote_datas[name]
            excel_array = local_datas[name]
            # if len(excel_array) == 0:
            #     print("name = %s, excel_array = %s " % (name, excel_array))

            #time_4 = time.clock()
            #print('读取某文件花费时间： %f'%(time_4-time_3))
            dif_array, dif_row_data, dif_column_data, dif_row_excel, dif_column_excel = check_datas(excel_array, data_array)
            #time_5 = time.clock()
            #print('比对花费时间： %f'%(time_5-time_4))
            if len(data_array) == 0:
                data_array = ['']
            if len(excel_array) == 0:
                excel_array = ['']
            #try:
            show_dif_ui(dif_array, dif_row_excel, dif_column_excel, dif_row_data, dif_column_data, tex, name, [data_array[0], excel_array[0]])
            tex.update()
            # except Exception:
            #     print('data_array = %s'%str(data_array))
            #     print('excel_array = %s'%str(excel_array))
            #     return
            #print('第%d个文件检查结束 《%s》,一共花费时间： %f'%(index, name, (time.clock()-time_1)))
            #index += 1
        #print('本次检查花费时间： %f'%(time.clock()-time_6))
        self.insert_info("检查完毕，一共%s张表!" % len(local_datas.keys()), 1, 1)
        messagebox.showinfo("提示", "检查完毕，一共%s张表!" % len(local_datas.keys()))


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
            if len(data_array) == 0:
                data_array = useserver['now'].get_table_row([name])
                data_array = dataanalyze.change_dic_by_name(data_array)
                #print('data_array = %s ' % data_array)
            else:
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
            # try:
            show_dif_ui(dif_array, dif_row_excel, dif_column_excel, dif_row_data, dif_column_data, tex, name, [data_array[0], excel_array[0]])
            tex.update()
        self.insert_info("检查完毕，一共%s张表!" % len(names.keys()), 1, 1)
        messagebox.showinfo("提示", "检查完毕，一共%s张表!" % len(names.keys()))
            # except Exception:
            #     print('data_array = %s'%str(data_array))
            #     print('excel_array = %s'%str(excel_array))
            #     return
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
        self.insert_info("检查完毕，一共%s张表!" % len(names.keys()), 1, 1)
        messagebox.showinfo("提示", "检查完毕，一共%s张表!" % len(names.keys()))


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

if __name__ == "__main__":

    def list2dict(obj, key=''):
        return dict(map(lambda n: (n["server_name"], n["server_id"]) if key in n['server_id'] else {}, obj))

    def check_json(path):
        import json
        with open(path, 'r') as f:
            ret = json.load(f)
        return ret
    print("111111111111")
    ret = check_json(r"E:\Application\test.json")
    print("type(ret) = %s " % type(ret))
    for i in ret.keys():
        print(i)
    print("data_jdbc= %s" % ret["date_jdbc"])
    print(list2dict(ret["date_jdbc"]))
    pass