#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:  BryanGa
@time:  2021/12/08
@des:   管理定时调度
"""

import os
import sqlite3

from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from tzlocal import get_localzone

JOBSTORES = {
    "default": SQLAlchemyJobStore(url="sqlite:////Users/bryanga/PycharmProjects/self_test/db/test_1.db")  # 数据库路径
}

EXECUTORS = {
    "default": ThreadPoolExecutor(20)
}

DB_PATH = db_path = "/db/test_1.db"
DB_CONNECTOR = sqlite3.connect(db_path)
CONN = DB_CONNECTOR.cursor()


class SchedulerManager:
    TIME_ZONE = get_localzone()
    SCHEDULER = BackgroundScheduler(jobstores=JOBSTORES, executors=EXECUTORS)

    def __init__(self, scheduler_type, db_type, time_zone=None):
        self.connector = None
        self.db_type = db_type

        self.crontrigger = None
        self.set_scheduler(scheduler_type)
        self.set_time_zone(time_zone)

    def set_time_zone(self, time_zone):
        if time_zone:
            self.TIME_ZONE = time_zone

    def set_scheduler(self, scheduler_type):
        if scheduler_type == "BackgroundScheduler":
            self.SCHEDULER = BackgroundScheduler(jobstores=JOBSTORES, executors=EXECUTORS)
        elif scheduler_type == "BlockingScheduler":
            self.SCHEDULER = BlockingScheduler(jobstores=JOBSTORES, executors=EXECUTORS)

    def set_connector(self, db_type, db_information={}):
        if db_type == "MySQL":
            self.connector = ""

        elif db_type == "Sqlite":
            self.connector = ""

    def modify_job(self):  # 修改job
        # todo: 修改job
        # todo:修改job作业时间
        pass

    def remove_job(self, job_id):
        if job_id is None or job_id == "":
            return
        self.SCHEDULER.remove_job(id=job_id)

    def add_job(self, config):
        # todo:添加job
        function_1 = config.get("function")
        trigger = config.get("trigger")
        time_zone = self.TIME_ZONE
        id_ = config.get("id")
        self.SCHEDULER.add_job(func=function_1, trigger=trigger, time=time_zone, id=id_)
        return True

    def show_job(self):
        # todo: 查看job
        pass

    @classmethod
    def set_crontrigger(cls, config):
        month = config.get("month", None)
        day = config.get("day", None)
        hour = config.get("hour", None)
        minute = config.get("minute", None)
        second = config.get("second", None)
        return CronTrigger(month=month, day=day, hour=hour, minute=minute, second=second,
                           timezone=cls.TIME_ZONE)  # 每天固定时间执行


def delete_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)


def function_1():
    print("--------- function_1 ----------")


if __name__ == "__main__":
    delete_db()
    scheduler_manager = SchedulerManager("BackgroundScheduler", "Sqlite")
    crontrigger_config = {"hour": 15, "minute": 11}
    scheduler_manager.set_crontrigger(crontrigger_config)
    job_config = {"function": function_1, "trigger": scheduler_manager.set_crontrigger(crontrigger_config), "id": "1"}
    scheduler_manager.add_job(job_config)
    t = scheduler_manager.SCHEDULER
    t.start()
    s = BlockingScheduler
    print("---tttt---")
