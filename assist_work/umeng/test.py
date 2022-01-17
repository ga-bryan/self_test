#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:  BryanGa
@time:  2022/01/10
@des:   友盟访问数据实验
"""
import requests
from flask import Flask, request

app = Flask(__name__)


@app.route("/")
def index():
    return "Hello World"


@app.route("/loadData", methods=['GET'])
def load_data():
    # request_data = request.get_json() or request.args
    requests.get("finplus.openapi.umeng.com/finplus/credit")


if __name__ == "__main__":
    app.run(host="0.0.0.0")
