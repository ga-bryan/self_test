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
from flask import Flask
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug import run_simple
from setting import PROJECT_PATH

from apps.send_file_app import app as send_file_app
from apps.send_data_app import app as send_data_app
from apps.show_app import app as show_app
from apps.index_app import app as index_app

from setting import SERVING_HOST, PORT, ONE_DAY_IN_SECONDS

DATA_SOURCE = os.path.join(PROJECT_PATH, "test_data")

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = DATA_SOURCE
app.url_map.strict_slashes = False

if __name__ == "__main__":
    # todo: add init_table
    apps = DispatcherMiddleware(
        app,
        {
            "/file": send_file_app,
            "/data": send_data_app,
            "/show": show_app,
            "": index_app
        }
    )
    run_simple(hostname=SERVING_HOST, port=PORT, application=apps, threaded=True)

    try:
        while True:
            time.sleep(ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        sys.exit(0)
