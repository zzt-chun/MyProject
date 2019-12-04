# -*- coding: utf-8 -*-
# @Time    : 2019/11/22 17:48
# @Author  : zzt
# @File    : download_data.py

import requests
from pb.proto_pb2 import DataComparisonRes, DataComparisonReq
from pb.login_pb2 import LoginReq, LoginRes, VerifyMailReq
from pb.base_pb2 import StringRes
from Util.uiShow import UiShow, pb2json


from pb.pbjson import dict2pb

class HttpClient(object):

    def __init__(self):
        self.host = "http://123.57.55.156:8003"
        self._url = ''
        self.cookie = {}
        self.headers = {
            "User-Agent": "UnityPlayer/2018.4.0f1 (UnityWebRequest/1.0, libcurl/7.52.0-DEV)",
            "Accept-Encoding": "identity",
            "Accept": "application/x-protobuf",
            "Content-Type": "application/x-protobuf",
            "X-Unity-Version": "2018.4.0f1",
            "Connection": "keep-alive"
        }

    def _request(self, data=None):
        ret = requests.request(method="PUT",
                               url=''.join([self.host, self._url]),
                               headers=self.headers,
                               cookies=self.cookie,
                               data=data
                               )
        return ret

    def download_content(self, data):
        self.set_url("/teamC/dataComparison")
        _data = dict2pb(DataComparisonReq, data).SerializeToString()
        ret = self._request(_data)
        res = DataComparisonRes()
        res.ParseFromString(ret.content)
        return res

    def login(self, id, pwd):
        self.set_url("/loginC/login")
        _data = LoginReq()
        _data.account_id = id
        _data.account_pwd = pwd
        self.cookie = {}
        _data = _data.SerializeToString()
        ret = self._request(_data)
        self.set_cookie(requests.utils.dict_from_cookiejar(ret.cookies))
        res = StringRes()
        res.ParseFromString(ret.content)
        return res

    def verification_email(self, msg):
        self.set_url("/loginC/verifyMail")
        _data = VerifyMailReq()
        _data.code = msg
        _data.language = 2
        _data = _data.SerializeToString()
        ret = self._request(_data)
        res = LoginRes()
        res.ParseFromString(ret.content)
        #UiShow().show("", pb2json(res))
        return res

    def set_url(self, url):
        self._url = url
        return self

    def set_cookie(self, cookies: {}):
        self._cookie = cookies
        self.cookie.update(cookies)
        self.cookie.update({"Path": "/"})


if __name__ == "__main__":
    from pb.proto_pb2 import DataComparisonReq
    # a = DataComparisonReq()
    # a.server_id = "test_1"
    # a.table_name.append('1')
    # a.table_name.append('2')
    data = {
        "server_id": "test_1",
        "table_name": ['1', '2'],
    }
    a = dict2pb(DataComparisonReq, data)
    print(a)

    # data = {
    #     "server_id": "basketball_data",
    #     "table_name": "t_version"
    # }
    # ret = Http().run(data)
    # print("ret.ret = ", ret.ret)
    # print("ret.res = ", ret.res)

    pass
