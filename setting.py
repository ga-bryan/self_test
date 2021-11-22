#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:  BryanGa
@time:  2021/07/07
@des:   全局设置
"""

import os

from utils.file_tools import get_project_base_path

# path
PROJECT_PATH = get_project_base_path()
DATA_PATH = os.path.join(get_project_base_path(), "test_data")

# database
MYSQL_HOST = "127.0.0.1"
MYSQL_USER = "root"
MYSQL_PWD = "123456"
MYSQL_DB = "db"
MYSQL_DB = "ppc"
MYSQL_PORT = 3306

# log
LOG_PATH = os.path.join(PROJECT_PATH, "log", "log.log")
LOG_LEVEL = "INFO"

# file type
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', "csv"])
