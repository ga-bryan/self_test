#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:  BryanGa
@time:  2021/11/22
@des:   
"""

import os
from flask import Flask, render_template, send_file
from setting import PROJECT_PATH

DATA_SOURCE = os.path.join(PROJECT_PATH, "test_data")

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = DATA_SOURCE


@app.route("/")
def index():
    return render_template("rain_star.html")


@app.route("/fireworks")
def fireworks():
    return render_template("fireworks.html")


@app.route("/downloadFile", methods=["GET"])
def upload_file():
    file_1 = os.path.join(PROJECT_PATH, "test_data", "data_simple_1.csv")
    file_2 = os.path.join(PROJECT_PATH, "test_data", "million.csv")
    return send_file(filename_or_fp=file_2)


if __name__ == "__main__":
    app.run()
