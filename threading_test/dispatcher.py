#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:  BryanGa
@time:  2022/01/26
@des:   监控数据库数据变化
"""

import threading

from db.models import DmsJob
from loguru import logger


class Cron(threading.Thread):
    def __init__(self, interval, first_interval=None, lock=None):
        super(Cron, self).__init__()
        self.interval = interval
        self.first_interval = first_interval
        self.lock = lock
        self.finished = threading.Event()
        if self.first_interval is None:
            self.first_interval = self.interval

    def cancel(self):
        self.finished.set()

    def run(self):
        def do():
            try:
                if not self.lock or self.lock.acquire(0):
                    self.run_do()
            except Exception as e:
                logger.exception(e)
                raise e
            finally:
                if self.lock and self.lock.locked():
                    self.lock.release()

        try:
            self.finished.wait(self.first_interval)
            if not self.finished.is_set():
                do()

            while True:
                self.finished.wait(self.interval)
                if not self.finished.is_set():
                    do()
        except Exception as e:
            logger.exception(e)
            raise e

    def run_do(self):
        pass


class Detector(Cron):
    def run_do(self):
        self.detect_readying_job()

    @classmethod
    def detect_readying_job(cls):

        ready_jobs = DmsJob.select_ready_job()
        for job in ready_jobs:
            # todo:清理存在很长时间的任务
            data_type = job.run_time_config.get("data_type")
            if not data_type:
                raise ValueError("please set data_type rightly")
            download_info = job.run_time_config
            job_id = job.job_code
            download_info["job_id"] = job_id
            try:
                if turn2data_source(data_type).check_if_download_success(
                        **download_info
                ):
                    job_logger(job_id).info("start to run job {}".format(download_info))
                    turn2data_source(data_type).load_data(job_id, download_info)
            except Exception as e:
                dete_logger.exception(e)
                dete_logger.error(
                    "The current job:{} raise error:{}".format(job_id, str(e))
                )
