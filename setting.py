#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:  BryanGa
@time:  2021/07/07
@des:   全局设置
"""

import os

from utils.path_utils import get_project_base_directory
from utils.file_utils import get_conf

# path
PROJECT_PATH = get_project_base_directory()
DATA_PATH = os.path.join(get_project_base_directory(), "test_data")

# database
MYSQL_HOST = get_conf("MYSQL_HOST")
MYSQL_USER = get_conf("MYSQL_USER", "root")
MYSQL_PASSWORD = get_conf("MYSQL_PASSWORD")
MYSQL_DB = get_conf("DB")
MYSQL_PORT = int(get_conf("PORT", 3306))

# log
LOG_PATH = os.path.join(PROJECT_PATH, "log", "log.log")
LOG_LEVEL = "INFO"

# server
ONE_DAY_IN_SECONDS = 60 * 60 * 24 * 1000

# file type
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', "csv"])
_CONFIG_FILE = "/Users/bryanga/PycharmProjects/self_test/config.yaml"


SERVING_HOST = "0.0.0.0"
PORT = 8088