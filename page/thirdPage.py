# -*- coding: utf-8 -*-
# @Time    : 2019/11/25 17:26
# @Author  : zzt
# @File    : thirdPage.py


import datetime
from tkinter import filedialog
import os
import tkinter as tk
from tkinter import ttk
import time
import re
import subprocess
import threading
import configparser

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

def get_now_time():
    return datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')

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
        if section_list == [] or section_list == ['account']:
            self.insert_info('一键配置文件《config.ini》不存在或破损', 1)
        else:
            if 'account' in section_list:
                section_list.remove('account')
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
            self.insert_info('请检查导入包是否为符合要求的.apk包, 或者路径有包含中文', 1, 2)
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

