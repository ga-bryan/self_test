#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:  BryanGa
@time:  2022/01/26
@des:   监控数据库数据变化
"""

import threading
from db.MySQL.mysql_model import CURSOR


class Dispatcher(threading.Thread):
    def __init__(self, name):
        super(threading, self).__init__(name)
        pass

    def run(self):
        sql = "select * from host_bill"
        data = CURSOR.execute(sql)

    pass


if __name__ == "__main__":
    sql = "select * from host_bill"
    data = CURSOR.execute(sql)
    print(data)
