#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:  BryanGa
@time:  2021/12/16
@des:   账单数据源配置
"""

from setting import MYSQL_DB, MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD
from peewee import MySQLDatabase, Model, FloatField, IntegerField, DateTimeField, CharField, BigIntegerField, SQL, \
    DateField, BigAutoField

DB = MySQLDatabase(
    MYSQL_DB,
    **{
        'charset': 'utf8',
        'sql_mode': 'PIPES_AS_CONCAT',
        'use_unicode': True,
        'host': MYSQL_HOST,
        'port': MYSQL_PORT,
        'user': MYSQL_USER,
        'password': MYSQL_PASSWORD,
    }
)


class BaseModel(Model):
    class Meta:
        database = DB

    def get_calculate_info(self, info_id):
        result = self.select().where(info_id == self.id)

        return result

    @classmethod
    def calculate_by_day(cls, infos):
        # todo:计算公式
        result = 0
        return result

    @classmethod
    def calculate_by_month(cls, infos):
        # todo:计算公式
        # todo：方案一查询当前月份的前面所有统计值做累加，加上今天的值
        # todo：方案二重新计算当月全部费用
        result = 0
        return result

    @classmethod
    def calculate_by_quarter(cls, infos):
        # todo:计算公式
        # todo：查询当前季度的前面所有统计值
        result = 0
        return result


class HostBill(BaseModel):
    auto_cost = FloatField(null=True)
    call_count = IntegerField(null=True)
    call_type = IntegerField(null=True)
    cost_type = IntegerField(null=True)
    created_at = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    data_code = CharField(null=True)
    data_id = BigIntegerField()
    data_version = CharField(null=True)
    data_version_id = BigIntegerField(null=True)
    date = DateField(null=True)
    edit_cost = FloatField(null=True)
    error_count = IntegerField(null=True)
    hit_count = IntegerField(null=True)
    id = BigAutoField()
    partner_id = BigIntegerField()
    partner_name = CharField(null=True)
    updated_at = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])

    class Meta:
        table_name = 'host_bill'


class DataSource(HostBill):
    class Meta:
        table_name = ""

    def __init__(self):
        super(DataSource, self).__init__()
        pass


class DataApply(BaseModel):
    class Meta:
        table_name = ""

    def __init__(self):
        super(DataApply, self).__init__()
        pass


if __name__ == "__main__":
    i = 8
    for i in range(i):

        if i > 5:
            i = 10
        print(i)
