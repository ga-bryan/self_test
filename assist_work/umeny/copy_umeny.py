#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:  BryanGa
@time:  2022/02/15
@des:   模拟
"""
import json

import pandas as pd
from flask import Flask, request, send_file
import os
import random

from utils.core_utils import generate_tmp_table_name
from utils.api_utils import json_response
from utils.path_utils import check_path

app = Flask(__name__)

app.url_map.strict_slashes = False
PROJECT_PATH = "/home/dppc/bryanga"
# PROJECT_PATH = "/Users/bryanga/PycharmProjects/self_test"

SERVING_HOST = "0.0.0.0"
PORT = 5001


@app.route("/uploadFile", methods=["GET"])
def upload_file():
    request_config = request.args.to_dict() or request.json or request.form.to_dict()
    bcid = request_config.get("bcid", None)
    check_path(os.path.join(PROJECT_PATH, "test_data", "send"))
    if bcid:
        path = os.path.join(PROJECT_PATH, "test_data", "send", bcid)
        return send_file(path_or_file=path)
    else:
        file_1 = os.path.join(PROJECT_PATH, "test_data", "send", "id.csv")
        return send_file(path_or_file=file_1)


@app.route("/batchComputeCalculate", methods=["POST"])
def batch_compute_calculate():
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
    config = {'taskIds': [file_name]}
    # return json_response(data=config)
    # return {"code": 200, "data": json.dumps(config)}
    return {"code": 200, "data": config}


@app.route("/batchCompute", methods=["POST"])
def batch_compute():
    check_path(os.path.join(PROJECT_PATH, "test_data", "send"))
    file_name = "8d5adba5-92ee-386f-89c1-44a284e9264a.csv"
    config = {'taskIds': [file_name]}
    # return {"code": 200, "data": json.dumps(config)}
    return {"code": 200, "data": config}


@app.route("/online", methods=["POST"])
def data_on_line():
    dimension = 10
    config = request.json or request.args.to_dict() or request.form.to_dict()
    id_ = config.get("idValue")
    result = {}
    if not id_:
        return json_response()
    for i in range(dimension):
        result['x{}'.format(i)] = str(random.random())

    return {"code": 200, "data": json.dumps({'response': {'tags': result}})}


if __name__ == "__main__":
    app.run(host=SERVING_HOST, port=PORT)
