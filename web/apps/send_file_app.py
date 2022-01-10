#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:  BryanGa
@time:  2021/12/29
@des:   传输数据或文件的app
"""

from flask import Flask, send_file
import os
from setting import PROJECT_PATH, SERVING_HOST

from utils.core_utils import generate_tmp_table_name
from utils.api_utils import json_response

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route("/uploadFile", methods=["GET"])
def upload_file():
    file_1 = os.path.join(PROJECT_PATH, "test_data", "data_simple_1.csv")
    # file_2 = os.path.join(PROJECT_PATH, "test_data", "million.csv")
    return send_file(path_or_file=file_1)


@app.route("/downloadFile", methods=["GET"])
def download_data():
    config_data = dict()
    config_data["http_url"] = 'http://{}:8080/file/uploadFile'.format(SERVING_HOST)
    data_root_path = os.path.join(PROJECT_PATH, "http_data")
    if not os.path.exists(data_root_path):
        os.makedirs(data_root_path)

    def save_data(root_path=data_root_path, url=None):
        if not url:
            raise ValueError("please check http_url is set")
        import requests
        save_path = os.path.join(root_path, generate_tmp_table_name())
        resp = requests.get(url)
        with open(save_path, "wb") as lf:
            lf.write(resp.content)
        return save_path

    file_name = save_data(url=config_data.get("http_url", None))
    config_data["file"] = file_name
    return json_response()


if __name__ == "__main__":
    app.run()