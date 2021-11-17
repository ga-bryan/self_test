#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:  BryanGa
@time:  2021/11/17
@des:   装饰器
"""

import os


def check_file_is_exist(function):  # 检查文件是否存在的装饰器

    def wrapper(path):
        if not os.path.exists(path):
            raise ValueError("Please check the file is real exist")
        try:
            return function(path)

        except Exception as e:
            return e

    return wrapper(path)


@check_file_is_exist
def read(path):
    with open(path, "rb") as f:
        return f.readline()


if __name__ == "__main__":
    path = "/Users/bryanga/PycharmProjects/self_test/utils/db_connect.py"
    read(path)
