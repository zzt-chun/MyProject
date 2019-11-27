# -*- coding: utf-8 -*-
# @Time    : 2019/11/25 17:17
# @Author  : zzt
# @File    : functionPageFrame.py
import tkinter as tk

#用于计数左边按钮数量， 目前最大数量为21， 若超过应相应添加下拉条
menus = []

def show_frame(self):
    for i in menus:
        if i[0] == self:
            if isinstance(i[1], type):
                i[1] = i[1](self)
            self.grid(row=0, column=2)
        else:
            i[0].grid_forget()

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