#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:  BryanGa
@time:  2021/12/07
@des:   计算账单
"""

parameters = {
    "calculate_id": "",
    "start_time": "",
    "end_time": "",
    "data_ids": ""
}

table_name = ""
connector = ()


def get_calculate_operator(parameters):
    get_data_information_sql = "select * from {} where time_1 >= {} and ".format(table_name)
    pass
    information = "do_select"
    return information


def calculate_by_day():
    # todo：确定每次计算id，每日的计算根据id进行录入
    # todo： 同一个计算id的前一日计算值
    return


def calculate_by_month():
    # todo：每月2号开始计算当月
    # todo: 同一个计算id的一个月内的日累计值
    return


def calculate_by_quarter():
    # todo: 2号开始检查季度归属
    # todo: 同一个计算id的一个季度内的月度累计值
    return


def get_month():
    # todo:获取当前时间的月份信息
    pass


def get_quarter():
    # todo: 获取当前时间的所属季度信息
    pass


def insert():
    # 新增
    return True


def update():
    # 更新
    return True
