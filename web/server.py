#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:  BryanGa
@time:  2021/11/22
@des:   
"""

import os
import sys
import time
from multiprocessing import Pool, cpu_count, Process, Queue

from flask import Flask
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug import run_simple
from setting import PROJECT_PATH

from apps.send_file_app import app as send_file_app
from apps.send_data_app import app as send_data_app
from apps.show_app import app as show_app
from apps.index_app import app as index_app
from apps.fraudulant_gold_flower import app as flower_app

from setting import SERVING_HOST, PORT, ONE_DAY_IN_SECONDS

DATA_SOURCE = os.path.join(PROJECT_PATH, "test_data")

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = DATA_SOURCE
app.url_map.strict_slashes = False

QUEUE = [Queue(10) for i in range(5)]


def add_task(queue):
    while 1:
        for i in range(10):
            queue.put(i)
        # time.sleep(4)
        # event.wait(4)
    # for i in range(10):
    #     queue.put(i)
    # time.sleep(4)


def worker(queue):
    while 1:
        # value = queue.get("1234")
        value = queue.get()
        print("---{}____".format(queue.qsize))
        if not value:
            print("当前没有待处理任务")
            time.sleep(5)
        print("----{}----".format(value))


if __name__ == "__main__":
    apps = DispatcherMiddleware(
        app,
        {
            "/file": send_file_app,
            "/data": send_data_app,
            "/show": show_app,
            "/flower": flower_app,
            "": index_app
        }
    )

    print("---hhh----")
    producer = Process(target=add_task, args=(QUEUE[0],), daemon=True)
    consumer = Process(target=worker, args=(QUEUE[0],), daemon=True)
    consumer.start()
    producer.start()
    run_simple(hostname=SERVING_HOST, port=PORT, application=apps, threaded=True)
    try:
        while True:
            time.sleep(ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        sys.exit(0)
