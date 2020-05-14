# -*- coding: utf-8 -*-
# @Time    : 2020/3/5 12:28
# @Author  : zzt
# @File    : closePage.py
from tkinter import messagebox
import tkinter as tk

def on_closing(root):
    top = tk.Toplevel()

    but1 = tk.Button(top, text='确认退出', width=12, command=lambda: root.destroy())
    but2 = tk.Button(top, text='取消退出', width=12, command=lambda: top.destroy())
    but1.pack(side=tk.LEFT)
    but2.pack(side=tk.RIGHT)



if __name__ == "__main__":
    root = tk.Tk()
    root.title('测试内部工具 v_2.2')
    root.resizable(0, 0)
    root.geometry("+500+200")
    root.protocol("WM_DELETE_WINDOW", on_closing(root))
    #on_closing(root)

    root.mainloop()