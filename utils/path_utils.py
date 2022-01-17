#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:  BryanGa
@time:  2021/12/29
@des:   
"""

import os


def get_project_base_directory(project_base=None):
    if project_base:
        return project_base
    PROJECT_BASE = os.path.abspath(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
    )
    return PROJECT_BASE


def check_path(path, mkdir=True):
    if not os.path.exists(path):
        if mkdir:
            os.makedirs(path)
