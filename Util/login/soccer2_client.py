# -*- coding: utf-8 -*-
# @Time    : 2020/4/17 12:28
# @Author  : zzt
# @File    : soccer2_client.py
import json

from Util.login.http_client import HttpClient
#import jsonpath
from pb.soccerPB.s_proto_pb2 import ServerInfoResS, DataComparisonReqS, DataComparisonResS
from Util.uiShow import pb2dict, except_ui_show, pb2json, dict2pb

class Soccer2HttpClient(HttpClient):

    def __init__(self, style, informer):
        super().__init__(style, informer)
        self.host = {
            #"最佳11人": "http://192.168.1.114:8687", #内网登录中心
            "最佳11人": "http://123.57.55.156:8004", #外网线上
            "最佳11人登录中心": "http://47.94.138.239:8002", #外网线上登录
            "干洋": "http://192.168.2.58:7002",

        }
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
            "Accept-Encoding": "gzip, deflate",
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/x-www-form-urlencoded",
            "Connection": "keep-alive"
        }
        self._headers = {
            "User-Agent": "UnityPlayer/2018.4.0f1 (UnityWebRequest/1.0, libcurl/7.52.0-DEV)",
            "Accept-Encoding": "identity",
            "Accept": "application/x-protobuf",
            "Content-Type": "application/x-protobuf",
            "X-Unity-Version": "2018.4.0f1",
            "Connection": "keep-alive"
        }
        self.method = "POST"

    def _login_head(self, _id, _pwd):
        self.style = "最佳11人登录中心"
        self.set_url("/session/login")
        ret = self._request({'userId': _id, "password": _pwd})
        self.set_cookie({
            "IAC-TOKEN": ret.json()["data"]['token'],
            "IAC-SID": ret.json()["data"]['sessionId'],
        })

    def download_content(self, data):
        self.set_url("/api/data/dataComparison")
        _data = dict2pb(DataComparisonReqS, data).SerializeToString()
        ret = self._request(_data)
        res = DataComparisonResS()
        res.ParseFromString(ret.content)
        return res


    def _get_jdbc(self):
        self.style = "最佳11人"
        self.headers = self._headers
        self.set_url("/api/serverC/serverInfoList")
        ret = self._request()
        res = ServerInfoResS()
        res.ParseFromString(ret.content)
        return res

    def login(self, account_info):
        self.informer.insert_info('正在登陆管理后台账号：%s ...' % account_info[0], 1)
        self._login_head(account_info[0], account_info[1])
        self.informer.insert_info('登陆管理后台账号成功。-》拉取服务器信息', 1, 1)
        ret = self._get_jdbc()
        ret = json.loads(pb2json(ret))
        self.informer.insert_info('拉取服务器信息', 1, 1)
        return ret


        # ret = self._get_jdbc()
        # if ret.ret != 0:
        #     print('ret.ret = ', ret.ret)
        #     return
        # return ret


    def set_cookie(self, cookies: {}):
        self.cookie = cookies

if __name__ == "__main__":
    cl = Soccer2HttpClient("最佳11人", '')
    #cl._login_head("li_test01", "li_test01")
    #print(cl.login(["li_test01", "li_test01"]))
    print(cl.login(["dengchun", "wckj123456"]))
    # params = [{'table_name': "t_team", "col_name": "team_id", "col_value": ["111mb", "1114a"]}]
    # data = {
    #     "server_id": "soccer3_001",
    #     "source_mark": "game",
    #     "query_type": 2,
    #     "query_param": params,
    # }
    # data_1 = {
    #     "server_id": "soccer3_001",
    #     "source_mark": "data",
    #     "query_type": 1,
    #     "query_param": [{"table_name": "t_cross_realm_activity_integral_award_rule", "col_name": "activity_type", "col_value": "308"}, {"table_name": "t_cross_realm_activity_rank_award_rule", "col_name": "level", "col_value": "1"}],
    # }
    # ret = cl.download_content(data)
    # ret = json.loads(pb2json(ret))
    #
    # print(ret)
