#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:  BryanGa
@time:  2021/10/29
@des:   文件的上传和下载
"""
import os

from flask import Flask, send_file, Response
from requests_toolbelt import MultipartEncoder
from setting import PROJECT_PATH

DATA_SOURCE = os.path.join(PROJECT_PATH, "test_data")
# ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', "csv"])
ALLOWED_EXTENSIONS = set(['json'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = DATA_SOURCE


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route("/")
def index():
    return "HelloWord"


@app.route("/downloadFile", methods=["GET"])
def upload_file():
    file_1 = os.path.join(PROJECT_PATH, "test_data", "data_simple_1.csv")
    file_2 = os.path.join(PROJECT_PATH, "test_data", "million.csv")
    return send_file(filename_or_fp=file_2)


if __name__ == "__main__":
    app.run()
