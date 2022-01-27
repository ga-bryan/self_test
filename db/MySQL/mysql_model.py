#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:  BryanGa
@time:  2022/01/26
@des:   mysql使用model
"""

import pymysql

DB_CONNECTOR = pymysql.connect(host='127.0.0.1',
                               user='root',
                               password='12345678',
                               database='sdn',
                               port=3306)

CURSOR = DB_CONNECTOR.cursor()