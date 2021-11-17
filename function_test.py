#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:  BryanGa
@time:  2021/11/09
@des:   python内置函数的实验
"""

import os
import importlib
from utils.file_tools import get_project_base_path

PROJECT_PATH = get_project_base_path()


def setattr_test(obj, key, value):
    """ setattr 如果obj具有key属性，赋值为value"""
    if hasattr(obj, key):
        setattr(obj, key, value)
    pass


def getattr_test(import_file, function_name):
    """ getattr 函数使用"""
    return getattr(import_file, function_name)


def import_module_test():
    """ importlib.import_module 学习"""
    module = "%s.%s" % ("learn_python", "test")  # 引用当前路径下的'learn_python模块下的test文件
    m = importlib.import_module(module)
    t = getattr_test(m, "calculate")(1, 2)  # 引用对应文件下的'calculate'


if __name__ == "__main__":
    import_module_test()
