# -*- coding: utf-8 -*-
# @Time    : 2019/11/25 17:27
# @Author  : zzt
# @File    : fourthPage.py

from tkinter import filedialog
import os
import tkinter as tk
import re
import subprocess
import datetime

class FourthPage():
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
                #用于检查adb命令返回的格式
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

def get_now_time():
    return datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')