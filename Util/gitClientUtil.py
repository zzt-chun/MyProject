# -*- coding: utf-8 -*-
# @Time    : 2020/4/14 19:56
# @Author  : zzt
# @File    : gitClientUtil.py

import gitlab

if __name__ == "__mian__":
    client = gitlab.Gitlab(r"http://git.wckj.com/", private_token="9zsoYLmazszeHvEi8DS9")
    client.auth()
    projects = client.projects.list()  # 获取所有项目信息
    project = client.projects.get(id=193)  # 获取对应项目
    logs = project.commits.list(ref_name="master", since="2020-03-05T11:01:23.000+07:00")  # 获取对应分支 某事件后的提交信息
