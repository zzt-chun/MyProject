# -*- coding: utf-8 -*-
# @Time    : 2020/4/17 11:45
# @Author  : zzt
# @File    : factory_client.py


from Util.login.basketball_http_client import BasketballHttpClient
from Util.login.soccer2_client import Soccer2HttpClient


class FactoryHttpClient(object):

    def create_client(self, style, *args, **kwargs):
        if "篮球" in style:
            return BasketballHttpClient(style, *args, **kwargs)
        elif "最佳11人" in style:
            return Soccer2HttpClient(style, *args, **kwargs)
