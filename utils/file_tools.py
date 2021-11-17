#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:  BryanGa
@des:   与文件有关的工具类方法
@time:  2021/07/07
"""

import os

import yaml


def get_project_base_path():
    return os.path.abspath(os.path.join(__file__, "../.."))


def load_yaml(yaml_path):
    with open(yaml_path) as f:
        values = yaml.safe_load(yaml_path, Loader=yaml.FullLoader)


if __name__ == "__main__":
    print(get_project_base_path())
