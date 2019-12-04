# -*- coding: utf-8 -*-
# @Time    : 2019/11/27 10:55
# @Author  : zzt
# @File    : uiShow.py

import tkinter as tk
import json
import sys
from tkinter import messagebox

class UiShow(object):

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("发送与接口数据展示工具")
        #self.root.resizable(0, 0)
        #self.f = tk.Frame(self.root, height=300, width=130)
        #self.f.pack()
        self.f0 = tk.LabelFrame(self.root, text="req")
        self.f1 = tk.LabelFrame(self.root, text="res")
        self.f0.pack(side="left", expand="yes", fill="both")
        self.f1.pack(side="right", expand="yes", fill="both")
        self.sb0 = tk.Scrollbar(self.f0)
        self.sb1 = tk.Scrollbar(self.f1)
        self.sb0.pack(side=tk.RIGHT, fill=tk.Y)
        self.sb1.pack(side=tk.RIGHT, fill=tk.Y)
        self.tex0 = tk.Text(self.f0, yscrollcommand=self.sb0.set)
        self.tex1 = tk.Text(self.f1, yscrollcommand=self.sb1.set)
        self.sb0.config(command=self.tex0.yview)
        self.sb1.config(command=self.tex1.yview)
        self.tex0.pack(expand="yes", fill=tk.BOTH)
        self.tex0.pack()
        self.tex1.pack(expand="yes", fill=tk.BOTH)
        self.tex1.pack()

    def show(self, req, res):
        req = req if not isinstance(req, dict) else json.dumps(req, sort_keys=True, indent=4)
        res = res if not isinstance(res, dict) else json.dumps(res, sort_keys=True, indent=4)
        self.tex0.insert(tk.END, req)
        self.tex1.insert(tk.END, res)
        self.root.mainloop()

def except_ui_show(func):
    def warpper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except:
            error_buf = sys.exc_info()
            messagebox.showerror(error_buf[0].__name__, error_buf[1])
    return warpper



import simplejson
from google.protobuf.descriptor import FieldDescriptor as FD


class ConvertException(Exception):
    pass

def dict2pb(cls, adict, strict=False):
    """
    Takes a class representing the ProtoBuf Message and fills it with data from
    the dict.
    """
    obj = cls()
    for field in obj.DESCRIPTOR.fields:
        if not field.label == field.LABEL_REQUIRED:
            continue
        if not field.has_default_value:
            continue
        if not field.name in adict:
            raise ConvertException('Field "%s" missing from descriptor dictionary.'
                                   % field.name)
    field_names = set([field.name for field in obj.DESCRIPTOR.fields])
    if strict:
        for key in adict.keys():
            if key not in field_names:
                raise ConvertException(
                    'Key "%s" can not be mapped to field in %s class.'
                    % (key, type(obj)))
    for field in obj.DESCRIPTOR.fields:
        if not field.name in adict:
            continue
        msg_type = field.message_type
        if field.label == FD.LABEL_REPEATED:
            if field.type == FD.TYPE_MESSAGE:
                for sub_dict in adict[field.name]:
                    item = getattr(obj, field.name).add()
                    item.CopyFrom(dict2pb(msg_type._concrete_class, sub_dict))
            else:
                list(map(getattr(obj, field.name).append, adict[field.name]))
        else:
            if field.type == FD.TYPE_MESSAGE:
                value = dict2pb(msg_type._concrete_class, adict[field.name])
                getattr(obj, field.name).CopyFrom(value)
            else:
                setattr(obj, field.name, adict[field.name])
    return obj


def pb2dict(obj):
    """
    Takes a ProtoBuf Message obj and convertes it to a dict.
    """
    adict = {}
    if not obj.IsInitialized():
        return None
    for field in obj.DESCRIPTOR.fields:
        if not getattr(obj, field.name):
            continue
        if not field.label == FD.LABEL_REPEATED:
            if not field.type == FD.TYPE_MESSAGE:
                adict[field.name] = getattr(obj, field.name)
            else:
                value = pb2dict(getattr(obj, field.name))
                if value:
                    adict[field.name] = value
        else:
            if field.type == FD.TYPE_MESSAGE:
                adict[field.name] = \
                    [pb2dict(v) for v in getattr(obj, field.name)]
            else:
                adict[field.name] = [v for v in getattr(obj, field.name)]
    return adict


def json2pb(cls, json, strict=False):
    """
    Takes a class representing the Protobuf Message and fills it with data from
    the json string.
    """
    return dict2pb(cls, simplejson.loads(json), strict)

def pb2json(obj):
    """
    Takes a ProtoBuf Message obj and convertes it to a json string.
    """
    return simplejson.dumps(pb2dict(obj), sort_keys=True, indent=4)




if __name__ == "__main__":
    pass