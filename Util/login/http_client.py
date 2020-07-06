# -*- coding: utf-8 -*-
# @Time    : 2020/4/16 10:56
# @Author  : zzt
# @File    : base_login.py

import requests


class HttpClient(object):

    def __init__(self, style, informer):
        self.host = ''
        self.style = style
        self._url = ''
        self.cookie = {}
        self.headers = {}
        self.method = ''
        self.informer = informer

    def _request(self, data=None):
        return requests.request(
            method=self.method,
            url="".join([self.host[self.style], self._url]),
            headers=self.headers,
            cookies=self.cookie,
            data=data
        )

    def download_content(self, data):
        raise NotImplementedError

    def login(self, account_info):
        raise NotImplementedError

    def set_url(self, url):
        self._url = url
        return True

    def set_cookie(self, cookies: {}):
        raise NotImplementedError
