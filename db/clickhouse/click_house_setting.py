#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:  BryanGa
@time:  2021/12/21
@des:   
"""

from clickhouse_driver import Client

host = "172.16.0.157"
port = "8123"
program = "9000"
program = "30208"
user = "default"
passwd = ""
db = "default"
engine = "MergeTree"

client = Client(host=host, port=program, user=user)
