# -*- coding: utf-8 -*-
# @Time    : 2020/5/16 19:33
# @Author  : zzt
# @File    : fifth.py

import datetime
import os
import sys
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import time
import threading

import gitlab
import gitlab.v4.objects

from page.topUiExcel import GitTopUiInfo


def get_now_time():
    return datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')


PROJECT_INFO = {
    # "篮球大师": ['http://git.wckj.com/', "Pf7-ssZdX9PE2xpmXg7n", 37],
    # "足球大师": ['http://git.wckj.com/', "Pf7-ssZdX9PE2xpmXg7n", 16],
    "最佳11人": ['http://git.wckj.com/', "Pf7-ssZdX9PE2xpmXg7n", 83],
}


class SixthPage(object):

    def __init__(self, parent):
        self.parent = parent
        self._branches = {}
        self._client = ''
        self.target_branche = ''
        self._master_name = "master"
        self.filters = ["Merge branch", "Lua"]
        self.target_branche_create_time = "2020-03-13"
        self.specify_folder = "Assets/StaticData"
        self.target_info = []
        self.create_buttons()

    def create_buttons(self):
        self.parent.pack_propagate(0)
        f0 = tk.Frame(self.parent, height=50, width=107)
        # f0.pack(anchor=tk.N, expand=True)
        f0.pack(anchor=tk.N)
        # 添加选择服务器下拉按钮
        com1 = ttk.Combobox(f0, state='readonly')
        com1.bind("<<ComboboxSelected>>", lambda *args: self.choose_project(com1, com2, ''))
        com1.set(' 选 择 项 目')
        com1['values'] = list(PROJECT_INFO.keys())
        com1.grid(row=0, column=0, padx=5, pady=3)
        # 添加选择数据库下拉按钮
        com2 = ttk.Combobox(f0, state='readonly', width=26)
        com2.bind("<<ComboboxSelected>>", lambda *args: self.choose_branch(com2))
        com2.set(' 选 择 分 支')
        com2.grid(row=0, column=1, padx=5, pady=3)
        but1 = tk.Button(f0, text='下载静态文件夹', width=18, height=2, command=lambda: self.button_download_target_files())
        but1.grid(row=0, column=2, padx=5, pady=3)
        # lf_2 = tk.LabelFrame(f0, text='可选')
        # lf_2.grid(row=1, column=0, columnspan=2, pady=3, padx=5)
        # but1 = tk.Button(f0, text='开  始  检  查', width=18, height=2, command=lambda: self.button_check_git())
        # but1.grid(row=0, column=2, padx=5, pady=3)
        # but2 = tk.Button(f0, text='打  印  差  异', width=18, height=2, command=lambda: self.button_download())
        # but2.grid(row=1, column=2, padx=5, pady=3)
        # tk.Label(lf_2, text="分支创建时间: ").grid(row=1, column=0, padx=5, pady=3)
        # ent1 = tk.StringVar()
        # tk.Entry(lf_2, text="2020-12-25", textvariable=ent1, width=26).grid(row=1, column=1, padx=5, pady=3)
        # tk.Button(lf_2, text="修改创建时间", width=10, command=lambda: self.change_date(ent1)).grid(row=1, column=2, padx=5,
        #                                                                                       pady=3)
        #
        # ent1.set(self.target_branche_create_time)
        # tk.Label(lf_2, text="过滤条件: ").grid(row=2, column=0, padx=5, pady=3)
        # ent2 = tk.StringVar()
        # tk.Entry(lf_2, text="Merge branch, Lua", textvariable=ent2, width=26).grid(row=2, column=1, padx=5, pady=3)
        # tk.Button(lf_2, text="修改过滤条件", width=10, command=lambda: self.change_filter(ent2)).grid(row=2, column=2, padx=5,
        #                                                                                         pady=3)
        # com3 = ttk.Combobox(lf_2, state='readonly', width=26)
        # com3.bind("<<ComboboxSelected>>", lambda *args: self.choose_branch_3(com3))
        # com3.set(' 选择目标分支（默认master）')
        # com3.grid(row=3, column=1, padx=5, pady=3)
        #
        # ent2.set("Merge branch, Lua")
        # 日志文本
        labelf = tk.LabelFrame(self.parent, text='日志文本：')
        labelf.pack(anchor=tk.N, expand=True)
        sb = tk.Scrollbar(labelf)
        sb.pack(side=tk.RIGHT, fill=tk.Y)
        self.tex = tk.Text(labelf, height=28, yscrollcommand=sb.set, width=107)
        self.tex.pack(side=tk.LEFT, fill=tk.BOTH)
        sb.config(command=self.tex.yview)
        self.tex.tag_config('tag1', foreground='green')
        self.tex.tag_config('tag2', foreground='red')
        # 添加其他按钮
        tk.Button(self.parent, text='保存日志', command=lambda: self.save_log(self.tex), width=15).pack(anchor=tk.S,
                                                                                                    side=tk.RIGHT,
                                                                                                    padx=3, pady=3)
        tk.Button(self.parent, text='清除日志', command=lambda: self.tex.delete(1.0, tk.END)).pack(anchor=tk.S,
                                                                                               side=tk.RIGHT, padx=5,
                                                                                               pady=3)

    def button_download_target_files(self):
        start_time = time.time()
        folder = self._project.repository_tree(self.specify_folder)
        first_directory = os.getcwd() + '\客户端静态文件'
        if not os.path.exists(first_directory):
            os.mkdir(first_directory)
        filename = ''.join([first_directory, '\\', get_now_time().replace(':', '_').replace(' ', '_')])
        os.mkdir(filename)
        threading_list = []
        for i in folder:
            if i['type'] == "tree":
                self.insert_info("文件夹:" + i['name'])
                deeper_file_name = filename + "/" + i['name'] + "/Cfgs"
                if not os.path.exists(filename + "/" + i['name']):
                    os.mkdir(filename + "/" + i['name'])
                if not os.path.exists(deeper_file_name):
                    os.mkdir(deeper_file_name)
                t = threading.Thread(target=self.download_single_file, args=(i['name'], deeper_file_name))
                t.start()
                threading_list.append(t)
        for i in threading_list:
            i.join()
        self.insert_info("下载完毕 and cost time: {}".format(time.time() - start_time), 1, 1)
        self.insert_info("文件夹所在位置 : {}".format(filename), 1, 1)





    def download_single_file(self, file_path, deeper_file_name):
        deeper_files = self._project.repository_tree(self.specify_folder + "/" + file_path + "/Cfgs", all=True, ref=self.target_branche)
        # print("deeper_files:", len(deeper_files))
        # index = 1
        for j in deeper_files:
            if not j['name'].endswith(".meta"):
                # index += 1
                # self.insert_info("第三层:" + j['name'] + ", style: " + j['type'])
                try:
                    with open(deeper_file_name + "/" + j['name'], "w", encoding='utf-8') as f:
                        _name = self.specify_folder + "/" + file_path + "/Cfgs/" + j['name']
                        # print(file_path + ": " + _name)
                        # print(deeper_file_name + "/" + j['name'])
                        # print("_name:", _name)
                        # continue
                        f.write(self._project.files.get(_name, ref=self.target_branche).decode().decode())
                except Exception:
                    print("exception file name: ", deeper_file_name + "/" + j['name'])
                    break
        # print("index： ", index)
    # 保存日志到当前目录（.txt）
    def save_log(self, e):
        array = e.get(1.0, tk.END)
        if len(array) == 1:
            messagebox.showerror('错误', '没有日志可保存!')
            return
        now_time = get_now_time()
        if not os.path.exists('配置文件夹'):
            os.mkdir('配置文件夹')
        if not os.path.exists('配置文件夹\日志'):
            os.mkdir('配置文件夹\日志')
        filename = now_time.replace(':', '_')
        filename = ''.join([os.getcwd(), '\配置文件夹\日志\分支提交差异日志_', filename, '.txt'])
        with open(filename, 'w') as f:
            f.write(array)
        self.insert_info('日志保存成功, 路径为<%s>\n' % filename, 1, 1)
        messagebox.showinfo('', '保存成功')

    def button_download(self):
        if len(self.target_info) <= 1:
            self.insert_info("未发现差异信息", 1, 1)
            return
        for _ in self.target_info[1:]:
            if _[-2] == 2:
                self.insert_info(str(_))

    def change_filter(self, ent):
        _value = ent.get()
        if len(_value.split(', ')) < 1:
            self.insert_info("输入过滤条件异常： %s !请检查是否满足格式xx, xx, xx" % _value, 1, 2)
            return
        self.filters = _value.split(', ')
        self.insert_info("修改过滤条件成功： %s" % _value, 1, 1)

    def change_date(self, ent):
        _value = ent.get()
        if len(_value.split('-')) == 3:
            self.target_branche_create_time = _value
            self.insert_info("分支创建时间修改成功： %s" % _value, 1, 1)
        else:
            self.insert_info("修改失败! 请检查时间格式是否满xx-xx-xx ：%s" % _value, 1, 2)

    def choose_project(self, com1, com2, com3):
        project_name = com1.get()
        try:
            self._client = gitlab.Gitlab(PROJECT_INFO[project_name][0], private_token=PROJECT_INFO[project_name][1])
            self._client.auth()
        except Exception:
            self.insert_info(str(sys.exc_info()), 1, 2)
        self.insert_info("登录成功", 1, 1)
        # projects = client.projects.list()  # 获取所有项目信息
        self._project = self._client.projects.get(id=PROJECT_INFO[project_name][2])  # 获取对应项目
        # logs = project.commits.list(ref_name="master", since="2020-03-05T11:01:23.000+07:00")  # 获取对应分支 某事件后的提交信息
        branches = self._project.branches.list(all=True, order_by="created_at")
        # files = self._project.files.get
        self._branches = {}
        for i in branches:
            self._branches.update({i.name: getattr(i, "commit").get('created_at')})
        com2['values'] = list(self._branches.keys())
        # com3['values'] = list(self._branches.keys())
        # for _ in branches:
        #    print(_)
        self.insert_info("获取《%s》项目分支信息成功！" % project_name, 1, 1)

    def choose_branch(self, com2):
        target = com2.get()
        if target not in self._branches.keys():
            self.insert_info("《%s》分支不存在！" % target, 1, 2)
            return
        self.target_branche = target
        self.insert_info("选中《%s》分支成功！" % target, 1, 1)

    def choose_branch_3(self, com3):
        target = com3.get()
        if target not in self._branches.keys():
            self.insert_info("《%s》分支不存在！" % target, 1, 2)
            return
        self._master_name = target
        self.insert_info("选中《%s》分支成功！" % target, 1, 1)

    def button_check_git(self):
        print('选中分支名为： %s， time: %s ' % (self.target_branche, self._branches[self.target_branche]))
        # create_time = self._client.commits.list(ref_name=self.target_branche)
        # brache = self._project.branches.get(self.target_branche)
        # print('目标分支信息： %s' % brache)
        # 1.5.0分支创建时间：2020-04-23 16:37:07 +0800
        # TODO 如果获取分支创建时间
        # self.target_branche_create_time = "2020-03-13 16:37:07 +0800"
        logs_target = self._project.commits.list(ref_name=self.target_branche, all=True,
                                                 since=self.target_branche_create_time)
        logs_master = self._project.commits.list(ref_name=self._master_name, all=True,
                                                 since=self.target_branche_create_time)
        self.target_info = [{"描述": 480, "日期": 120, "作者": 40, "提交id": 160}]
        master_info = [self.target_info[0]]
        # index = 3(过滤) or 2（未匹配到） or 1（匹配成功） 0(无色)
        for info in logs_target:
            index = 0
            if self.filter_title(self.filters, info.title):
                index = 3
            self.target_info.append([info.title, info.created_at[:-10], info.committer_name, info.id, index, 0])
        for info in logs_master:
            index = 0
            if self.filter_title(self.filters, info.title):
                index = 3
            master_info.append([info.title, info.created_at[:-10], info.committer_name, info.id, index, 0])
        del logs_target
        del logs_master
        index_tar = 0
        for info in self.target_info[1:]:
            index_tar += 1
            # 不匹配过滤单位
            if info[-2] == 3:
                continue
            exist = False
            index_mat = 0
            for _info in master_info[1:]:
                index_mat += 1
                # 不匹配过滤单位
                if info[-2] == 3:
                    continue
                if info[0] == _info[0]:
                    info[-2] = 1
                    info[-1] = index_mat
                    _info[-2] = 1
                    _info[-1] = index_tar
                    print("找到相同项： %s" % info[0])
                    exist = True
                    continue
            if not exist:
                info[-2] = 2
        for _ in self.target_info[1:]:
            if _[-2] == 2:
                print(str(_))
        GitTopUiInfo("master与分支提交检查", master_info, self.target_info)

    def insert_info(self, information, use_time=0, tag=0):
        if use_time:
            time = get_now_time() + ': '
        else:
            time = ''
        if tag == 0:
            this_tag = ''
        elif tag == 1:
            this_tag = 'tag1'
        elif tag == 2:
            this_tag = 'tag2'
        self.tex.insert(tk.END, time + information + '\n', this_tag)

    def filter_title(self, rule, target):
        if not isinstance(rule, list):
            rule = [rule]
        for _ in rule:
            if _ in target:
                return True
        return False
