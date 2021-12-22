#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:  BryanGa
@time:  2021/12/21
@des:   
"""

from clickhouse_driver import Client

host = "192.168.1.180"
port = "8123"
program = "9000"
user = "default"
passwd = ""
engine = "MergeTree"

client = Client(host=host, port=program, user=user)
