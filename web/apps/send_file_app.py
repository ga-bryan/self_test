#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:  BryanGa
@time:  2021/12/29
@des:   传输数据或文件的app
"""
import json

import pandas as pd
from flask import Flask, request, send_file
import os
import random
from setting import PROJECT_PATH, SERVING_HOST

from utils.core_utils import generate_tmp_table_name
from utils.api_utils import json_response
from utils.path_utils import check_path

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route("/uploadFile", methods=["GET"])
def upload_file():
    request_config = request.args.to_dict()
    filename = request_config.get("filename")
    check_path(os.path.join(PROJECT_PATH, "test_data", "send"))
    if not filename:
        file_1 = os.path.join(PROJECT_PATH, "test_data", "data_simple_1.csv")
        return send_file(path_or_file=file_1)
    else:
        path = os.path.join(PROJECT_PATH, "test_data", "send", filename)
        return send_file(path_or_file=path)


@app.route("/upload/file/<filename>", methods=["POST"])
def upload_file_by_file(filename):
    """ 发起请求时直接在路径中带上文件名就可以 /upload/file/tt.csv """
    if not filename:
        file_1 = os.path.join(PROJECT_PATH, "test_data", "data_simple_1.csv")
        return send_file(path_or_file=file_1)
    else:
        path = os.path.join(PROJECT_PATH, "test_data", "send", filename)
        return send_file(path_or_file=path)


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


@app.route("/batchCompute", methods=["POST"])
def batch_compute():
    import time
    request_config = request.form.to_dict()
    time.sleep(30)
    check_path(os.path.join(PROJECT_PATH, "test_data", "send"))
    check_path(os.path.join(PROJECT_PATH, "test_data", "receive"))
    dimension = 10
    file = request.files["file"]
    tmp_path = os.path.join(PROJECT_PATH, "test_data", "receive", generate_tmp_table_name())
    file.save(tmp_path)
    df = pd.read_csv(tmp_path)
    high = len(df)
    result = []
    for i in range(high):
        result.append([random.random() for i in range(dimension)])
    file_name = generate_tmp_table_name()
    result_path = os.path.join(PROJECT_PATH, "test_data", "send", file_name)
    result_df = pd.concat(
        [df, pd.DataFrame(result, columns=["x{}".format(i) for i in range(dimension)])],
        axis=1)
    result_df.to_csv(result_path, index=0)
    stat_time = request_config.get("stat_time")
    config = {"url": "http://192.168.1.88:8080/file/uploadFile", "filename": file_name,
              "stat_time": stat_time}
    return json_response(data=config)


if __name__ == "__main__":
    app.run()
