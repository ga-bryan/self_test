#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:  BryanGa
@time:  2021/12/03
@des:   定时任务
"""

from pytz import utc
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.date import DateTrigger
from apscheduler.triggers.cron import CronTrigger
from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore


def calculate():
    sum_ = 1 + 1 + 1
    print(sum_)


if __name__ == "__main__":
    executors = {
        "default": ThreadPoolExecutor(20)
    }
    jobstores = {
        "default": SQLAlchemyJobStore(url="sqlite:////Users/bryanga/PycharmProjects/self_test/db/test.db")  # 数据库路径
    }
    scheduler = BlockingScheduler(jobstores=jobstores, executors=executors)
    intervalTriggers = IntervalTrigger(seconds=1)  # 时间间隔
    dateTriggers = DateTrigger(run_date="2021-12-06 18:35:00")  # 时间点
    cronTrigger_day = CronTrigger(hour=19, minute=40, second=0)  # 每天固定时间执行
    cronTrigger_year = CronTrigger(month=12, hour=19, minute=41, second=0)  # 每年固定时间执行
    scheduler.add_job(calculate, intervalTriggers, id="1_2")
    scheduler.start()
