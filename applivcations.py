import tkinter as tk
import base64
import os
from resource import pics
from page.firstPage import FirstPage
from page.secondPage import SecondPage
from page.thirdPage import ThirdPage
from page.fifthPage import FifthPage
from page.functionPageFrame import FunctionPageFrame

root = tk.Tk()
root.title('测试内部工具')
root.resizable(0, 0)
root.geometry("+500+200")

#读取已经转码成.py格式的资源文件
for name in pics.keys():
    #生成临时图片
    tmp = open(name, 'wb')
    tmp.write(base64.b64decode(pics[name]))
    tmp.close()
    pics[name] = tk.PhotoImage(file=name)
    #删除临时图片
    os.remove(name)

#test一下
#root.iconbitmap('D:/MyProject/Applications/logo_3.ico')
#root.geometry('')

rb_v = tk.StringVar()
f0 = tk.Frame(root, height=600, width=130)
f0_1 = tk.Frame(root, height=600, width=5, bg='aqua')
f0_1.grid(row=0, column=1)
f0.grid(row=0, column=0)
#第一页
f1 = FunctionPageFrame(root, f0, rb_v, FirstPage, text='excel比对工具', photo=pics['logo_29x16.jpg'])
f1.grid_forget()
#第二页
f2 = FunctionPageFrame(root, f0, rb_v, SecondPage, text='服务器配置检查', photo=pics['logo_29x16.jpg'])
f2.grid_forget()
#第三页
f3 = FunctionPageFrame(root, f0, rb_v, ThirdPage, text='monkey', photo=pics['logo_29x16.jpg'])
f3.grid_forget()
#第四页
f4 = FunctionPageFrame(root, f0, rb_v, FifthPage, text='一键截图与装包', photo=pics['logo_29x16.jpg'])
f4.grid_forget()
#第五页
f5 = FunctionPageFrame(root, f0, rb_v, text='待添加', photo=pics['logo_29x16.jpg'])
tk.Label(f5, image=pics['log.jpg']).pack()
tk.Label(f5).pack()

if __name__ == '__main__':
    root.mainloop()
