#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:  BryanGa
@time:  2021/12/29
@des:   传输数据
"""

from flask import Flask, request
import random
from utils.api_utils import json_response

app = Flask(__name__)


@app.route("/jsonData")
def send_json():
    return json_response()


@app.route("/online", methods=["POST"])
def data_on_line():
    dimension = 10
    config = request.json or request.args.to_dict()
    data = config.get("data")
    result = [["id"] + ["x{}".format(i) for i in range(dimension)]]
    if not data:
        return json_response()
    for d in data:

        result.append([str(d).strip()] + [str(random.random()) for i in range(dimension)])

    return json_response(data={"data": result})
