#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:  BryanGa
@time:  2021/12/07
@des:   计算调度
"""
import time
import os
# from zoneinfo import ZoneInfo
from tzlocal import get_localzone
from pytz import utc
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger
from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.events import EVENT_JOB_ERROR, EVENT_JOB_MISSED, EVENT_JOB_EXECUTED

# todo：如何设置时区，配置back调度方式
# tzinfo = get_localzone()
tzinfo = utc

TRIGGER_DAY = IntervalTrigger(days=1)
TRIGGER_TEST = IntervalTrigger(seconds=3)
TRIGGER_TEST = IntervalTrigger(seconds=30)

day = 15
hour = 16
minute = 5
seconds = 5
# CRONTRIGGER_DAY = CronTrigger(hour=hour, minute=minute, second=seconds, timezone=tzinfo)  # 每天固定时间执行
CRONTRIGGER_DAY = CronTrigger(hour=hour, minute=minute, second=seconds)  # 每天固定时间执行
CRONTRIGGER_MONTH = CronTrigger(day=day, hour=hour, minute=minute, second=seconds, timezone=tzinfo)  # 每月时间执行
CRONTRIGGER_QUARTERLY = CronTrigger(hour=hour, minute=minute, second=seconds, timezone=tzinfo)  # 每季度固定时间执行

executors = {
    "default": ThreadPoolExecutor(20)
}
db_path = "/db/test_1.db"

jobstores = {
    "default": SQLAlchemyJobStore(url="sqlite:////Users/bryanga/PycharmProjects/self_test/db/test_1.db")  # 数据库路径
}

job_defaults = {
    'coalesce': False,
    'max_instances': 3
}

def function_1():
    with open("/Users/bryanga/PycharmProjects/self_test/db/test_1.txt", mode="w") as f:
        f.write("---func1   ---")
    print("function_1 start time {}".format(time.time()))
    print("--------- function_1 ----------")
    # time.sleep(2)
    print("--------- function_1 plus ----------")
    print("function_1 end time {}".format(time.time()))
    pass


def function_2():
    with open("/Users/bryanga/PycharmProjects/self_test/db/test_2.txt", mode="w") as f:
        f.write("---func2    ---")
    print("function_2 start time {}".format(time.time()))
    print("--------- function_2 -----------")
    # todo: 添加时间条件检测
    print("--------- function_2 plus -----------")
    print("function_2 end time {}".format(time.time()))
    pass


def function_3():
    print("function_3 start time {}".format(time.time()))

    # todo:添加时间条件检测
    print("----- function_3 -------")
    print("--------- function_3 plus -----------")
    print("function_3 end time {}".format(time.time()))
    pass


def listener(event):
    # todo: 完善监听方法
    job = scheduler.get_job(job_id=event.job_id)
    if not event.exception:
        print("There is nothing exception")
    else:
        print(event.exception)


def delete_db():
    if os.path.exists(db_path):
        os.remove(db_path)


if __name__ == "__main__":
    delete_db()
    scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults)
    # scheduler = BlockingScheduler(jobstores=jobstores, executors=executors)
    scheduler.add_job(func=function_1, trigger=CRONTRIGGER_DAY, id="test_job_1")
    scheduler.add_job(func=function_2, trigger=CRONTRIGGER_DAY, id="test_job_2")
    # scheduler.remove_job("ttt")

    scheduler.add_listener(listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR | EVENT_JOB_MISSED)
    scheduler.start()
    print('---tttt---')
