#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:  BryanGa
@time:  2021/11/30
@des:   临时
"""

import json

t = """
{
    "file": "tmp.csv",
    "id_delimiter": ",",
    "head": 1,
    "partition": 4,
    "work_mode": 1,
    "backend": 0,
    "namespace": "tmp",
    "table_name": "tmp",
    "task_cores": 2,
    "http_url": "http://127.0.0.1:5000/uploadFile",
    "use_local_data": 0
}
"""

{'retcode': 0, 'retmsg': 'success', 'data': {'update_server': {'studio': {'host': '172.16.0.162', 'port': 8098}}}}
{'retcode': 0, 'retmsg': 'success', 'data': {'update_server': {'studio': {'host': '172.16.0.162', 'port': 8098}}}}
# print(json.loads(t))
t = [1, 2]
print(t[0:-1])
