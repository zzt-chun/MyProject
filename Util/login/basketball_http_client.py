# -*- coding: utf-8 -*-
# @Time    : 2020/4/16 14:52
# @Author  : zzt
# @File    : basketball_http_client.py

import requests

from Util.login.http_client import HttpClient
from Util.mailUtil import MailClient
from Util.uiShow import pb2dict
from pb.basketballPB.base_pb2 import StringRes
from pb.basketballPB.login_pb2 import LoginReq, LoginRes, VerifyMailReq
from pb.basketballPB.proto_pb2 import DataComparisonRes, DataComparisonReq
from pb.pbjson import dict2pb


class BasketballHttpClient(HttpClient):

    def __init__(self, style, informer):
        super().__init__(style, informer)
        self.host = {
            "篮球国内": "http://123.57.55.156:8003",
            "篮球港澳台": "http://47.90.44.198:8002",
        }
        self.headers = {
            "User-Agent": "UnityPlayer/2018.4.0f1 (UnityWebRequest/1.0, libcurl/7.52.0-DEV)",
            "Accept-Encoding": "identity",
            "Accept": "application/x-protobuf",
            "Content-Type": "application/x-protobuf",
            "X-Unity-Version": "2018.4.0f1",
            "Connection": "keep-alive"
        }
        self.method = "PUT"

    def _login_head(self, _id, _pwd):
        self.set_url("/loginC/login")
        _data = LoginReq()
        _data.account_id = _id
        _data.account_pwd = _pwd
        self.cookie = {}
        _data = _data.SerializeToString()
        ret = self._request(_data)
        self.set_cookie(requests.utils.dict_from_cookiejar(ret.cookies))
        res = StringRes()
        res.ParseFromString(ret.content)
        return res

    def _get_email_msg(self, _id, _pwd):
        # 登录邮箱
        self.informer.insert_info('正在登陆验证码邮件账号：%s...' % _id, 1)
        mc = MailClient(_id, _pwd)
        self.informer.insert_info('登陆验证码邮件账号成。 -》下一步验证邮箱', 1, 1)
        _msg = mc.find_my_mail('account@galasports.com', 'The server authentication code-GALA Sports').split(':')[1][:4]
        mc.close()
        return _msg

    def login(self, account_info):
        # 先登录
        self.informer.insert_info('正在登陆管理后台账号：%s ...' % account_info[0], 1)
        self._login_head(account_info[0], account_info[1])
        self.informer.insert_info('登陆管理后台账号成功。-》下一步登录邮箱', 1, 1)
        # 登录邮箱  获取验证码
        msg = self._get_email_msg(account_info[2], account_info[3])
        self.informer.insert_info('获取邮箱验证码《%s》成功. —》下一步验证....' % msg, 1, )
        # 发送验证码
        ret = self._verification_email(msg)
        if ret.ret != 0:
            self.informer.insert_info("验证失败： %s" % ret.msg)
            return
        return pb2dict(ret)

    def download_content(self, data):
        self.set_url("/teamC/dataComparison")
        _data = dict2pb(DataComparisonReq, data).SerializeToString()
        ret = self._request(_data)
        res = DataComparisonRes()
        res.ParseFromString(ret.content)
        return res

    def _verification_email(self, msg):
        self.set_url("/loginC/verifyMail")
        _data = VerifyMailReq()
        _data.code = msg
        _data.language = 2
        _data = _data.SerializeToString()
        ret = self._request(_data)
        res = LoginRes()
        res.ParseFromString(ret.content)
        # UiShow().show("", pb2json(res))
        return res

    def set_cookie(self, cookies: {}):
        self.cookie.update(cookies)
        self.cookie.update({"Path": "/"})
