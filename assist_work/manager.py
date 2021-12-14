#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:  BryanGa
@time:  2021/12/08
@des:   管理定时调度
"""
import sqlite3

DB_PATH = db_path = "/Users/bryanga/PycharmProjects/self_test/db/test_1.db"
DB_CONNECTOR = sqlite3.connect(db_path)
CONN = DB_CONNECTOR.cursor()

# todo：配置定时任务参数
scheduler = ""


class SchedulerManager:
    def __init__(self):
        self.db = None

    def modify_job(self):  # 修改job
        # todo: 修改job
        # todo:修改job作业时间
        pass

    def delete_job(self, job_id):  # 根据id,删除数据库对应的数据记录
        delete_sql = "delete from table where id = {}".format(job_id)

        CONN.execute(delete_sql)
        return True

    def remove_job(self):
        pass


# todo:添加job
def add_job(*args, **kwargs):
    function_1 = kwargs.get("function_1")
    trigger = kwargs.get("trigger")
    time_zone = kwargs.get("TIME_ZONE")
    id_ = kwargs.get("id")
    scheduler.add_job(func=function_1, trigger=trigger, time=time_zone, id=id_)
    return True


# todo: 查看job
def show_job():
    pass
