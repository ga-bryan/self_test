#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:  BryanGa
@time:  2021/12/29
@des:   
"""

from flask import jsonify


def json_response(status=200, msg="success", data=None):
    return jsonify({"status": status, "msg": msg, "data": data})
