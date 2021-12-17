#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:  BryanGa
@time:  2021/12/16
@des:   账单数据源配置
"""


# todo：配置数据库

class Base:
    def __init__(self, table, connector):
        self.table = table
        self.connector = connector
        pass

    def get_calculate_info(self, info_id):
        sql = "select * from {} where id = {}".format(self.table, info_id)
        result = self.connector.execute(sql)

        return result

    @classmethod
    def calculate_by_day(cls, info):
        # todo:计算公式
        result = 0
        return result

    @classmethod
    def calculate_by_month(cls, info):
        # todo:计算公式
        result = 0
        return result

    @classmethod
    def calculate_by_quarter(cls, info):
        # todo:计算公式
        result = 0
        return result

    @classmethod
    def deal_info_from_db(cls, info):
        # todo: deal info
        return info


class DataSource(Base):
    def __init__(self, table, connector):
        super(DataSource, self).__init__(table, connector)
        pass


class DataApply(Base):
    def __init__(self, table, connector):
        super(DataApply, self).__init__(table, connector)
        pass


if __name__ == "__main__":
    pass
