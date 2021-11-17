#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:  BryanGa
@time:  2021/10/19
@des:   
"""

from flask import Flask

manager = Flask(__name__)


@manager.route("/test_information", methods=['POST'])
def test_information():
    return "success"
