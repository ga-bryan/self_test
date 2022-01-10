#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:  BryanGa
@time:  2021/11/17
@des:   装饰器
"""

import os
from functools import wraps

from loguru import logger

path = "/utils/db_connect_utils.py"


def check_file_is_exist(function):
    """ 检查文件是否存在的装饰器 """
    """ 装饰函数的装饰器只需要设置函数参数 """

    @wraps(function)
    def inner(path):
        """ 此处的参数不用通过装饰器来传递，和要修饰的函数保持一致即可 """
        if not path:
            raise ValueError("Please check the file is set rightly")
        elif os.path.exists(path):
            raise ValueError("Please check the file is real exist")
        try:
            return function(path)

        except Exception as e:
            return e

    return inner


@check_file_is_exist
def read(path):
    with open(path, "r") as f:
        return f.readline()


# def singleton(cls, *args, **kw):
#     """ 单例模式装饰器 """
#     instances = {}
#
#     def _singleton():
#         key = str(cls) + str(os.getpid())
#         if key not in instances:
#             instances[key] = cls(*args, **kw)
#         return instances[key]
#
#     return _singleton


def exception(func):
    """ 捕捉异常装饰器 """

    @wraps(func)
    def inner(**kwargs):
        try:
            res = func(**kwargs)
        except Exception as e:
            logger.exception(e)
            return str(e)
        return res

    return inner


if __name__ == "__main__":
    path = "/utils/db_connect_utils.py"
    read(path)
    # america()
