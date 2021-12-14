#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:  BryanGa
@time:  2021/12/07
@des:   计算调度
"""
import time
import os

import pytz
from backports.zoneinfo import ZoneInfo
from backports import zoneinfo
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger
from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.events import EVENT_JOB_ERROR, EVENT_JOB_MISSED, EVENT_JOB_EXECUTED

# TIME_ZONE = pytz.timezone('Asia/Beijing')
TIME_ZONE = pytz.timezone('Asia/Shanghai')

tzinfo = ZoneInfo("Europe/Minsk")
tzinfo = zoneinfo("Europe/Minsk")

TRIGGER_DAY = IntervalTrigger(days=1)
TRIGGER_TEST = IntervalTrigger(seconds=3)
TRIGGER_TEST = IntervalTrigger(seconds=30)

hour = 12
minute = 40
seconds = 5
CRONTRIGGER_DAY = CronTrigger(hour=hour)  # 每天固定时间执行
CRONTRIGGER_DAY = CronTrigger(hour=hour, timezone=tzinfo)  # 每天固定时间执行
# CRONTRIGGER_MONTH = CronTrigger(hour=hour, minute=minute, timezone=tzinfo)  # 每天固定时间执行
# CRONTRIGGER_QUARTERLY = CronTrigger(hour=hour, minute=minute, second=seconds, timezone=tzinfo)  # 每天固定时间执行

executors = {
    "default": ThreadPoolExecutor(20)
}
db_path = "/Users/bryanga/PycharmProjects/self_test/db/test_1.db"
if os.path.exists(db_path):
    os.remove(db_path)

jobstores = {
    "default": SQLAlchemyJobStore(url="sqlite:////Users/bryanga/PycharmProjects/self_test/db/test_1.db")  # 数据库路径
}

scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors)


# scheduler = BlockingScheduler(jobstores=jobstores, executors=executors)


def function_1():
    print("function_1 start time {}".format(time.time()))
    print("--------- function_1 ----------")
    # time.sleep(2)
    print("--------- function_1 plus ----------")
    print("function_1 end time {}".format(time.time()))
    pass


def function_2():
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


scheduler.add_job(func=function_1, trigger=TRIGGER_TEST, time=TIME_ZONE, id="test_job_1")
scheduler.add_job(func=function_2, trigger=TRIGGER_TEST, time=TIME_ZONE, id="test_job_2")
# scheduler.add_job(func=function_1, trigger=TRIGGER_DAY, time=TIME_ZONE)
# scheduler.add_job(func=function_2, trigger=TRIGGER_DAY, time=TIME_ZONE)
# scheduler.add_job(func=function_3, trigger=TRIGGER_DAY, time=TIME_ZONE)
# scheduler.add_job(func=function_1, trigger=CRONTRIGGER_DAY, id="t", time=TIME_ZONE)
# scheduler.add_job(func=function_2, trigger=CRONTRIGGER_MONTH, id="tt", time=TIME_ZONE)
# scheduler.add_job(func=function_3, trigger=CRONTRIGGER_QUARTERLY, id="ttt", time=TIME_ZONE)
# scheduler.remove_job("ttt")

scheduler.add_listener(listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR | EVENT_JOB_MISSED)

if __name__ == "__main__":
    scheduler.start()
