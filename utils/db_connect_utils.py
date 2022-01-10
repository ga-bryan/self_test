#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:  BryanGa
@time:  2021/07/07
@des:   数据库链接工具方法
"""
from peewee import MySQLDatabase

import setting as settings

MYSQL_DB = MySQLDatabase(
    settings.MYSQL_DB,
    **{
        'charset': 'utf8mb4',
        'sql_mode': 'PIPES_AS_CONCAT',
        'use_unicode': True,
        'host': settings.MYSQL_HOST,
        'port': settings.MYSQL_PORT,
        'user': settings.MYSQL_USER,
        'password': str(settings.MYSQL_PWD),
    }
)
