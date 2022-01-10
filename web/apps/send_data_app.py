#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:  BryanGa
@time:  2021/12/29
@des:   传输数据
"""

from flask import Flask
from utils.api_utils import json_response

app = Flask(__name__)


@app.route("/jsonData")
def send_json():
    return json_response
