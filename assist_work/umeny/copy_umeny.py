#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:  BryanGa
@time:  2022/02/15
@des:   模拟友盟
"""
import json
import zipfile
import pandas as pd
from flask import Flask, request, send_file, jsonify, send_from_directory
import os
import random
import base64
import uuid
import threading
import time

app = Flask(__name__)

app.url_map.strict_slashes = False


def get_project_base_directory(project_base=None):
    if project_base:
        return project_base
    project_base = os.path.abspath(
        os.path.dirname(os.path.realpath(__file__))
    )
    return project_base


PROJECT_PATH = get_project_base_directory()

SERVING_HOST = "0.0.0.0"
PORT = 5001


def check_path(path, mkdir=True):
    if not os.path.exists(path):
        if mkdir:
            os.makedirs(path)


def load_limit_id():
    path = os.path.join(PROJECT_PATH, "test_data", "limit")
    check_path(path)
    limit_csv = os.path.join(path, "breast_hetero_host.csv")
    return [cell[0] for cell in pd.read_csv(limit_csv, header=0, usecols=["id"], dtype="str").values.tolist()]


LIMITED_ID = load_limit_id()


def string_to_byte(string_):
    return base64.b64encode(string_.encode("utf-8"))


def byte_to_string(bytes):
    return bytes.decode(encoding="utf-8")


def base64_encode(string_):
    return byte_to_string(string_to_byte(string_))


class IdCounter:
    _lock = threading.RLock()

    def __init__(self, counter=0):
        self._count = counter

    @property
    def incr(self, step=1):
        with self._lock:
            self._count += step
            return self._count


id_counter = IdCounter()


def generate_tmp_table_name():
    return "{}.csv".format(
        uuid.uuid3(
            uuid.NAMESPACE_DNS,
            base64_encode(str(id_counter.incr) + str(time.time()))
        )
    )


def json_response(status=200, msg="success", data=None):
    return jsonify({"status": status, "msg": msg, "data": data})


@app.route("/uploadFile", methods=["GET"])
def upload_file():
    request_config = request.args.to_dict() or request.json or request.form.to_dict()
    bcid = request_config.get("bcId", None)
    stat_time = request_config.get("stat_time", None)
    count = request_config.get("count", None)
    check_path(os.path.join(PROJECT_PATH, "test_data", "send"))
    if bcid:
        if str(bcid) == "6666":
            bcid = "feature.csv"
        bcid_path = os.path.join(PROJECT_PATH, "test_data", "send", bcid)
        if count:
            bcid_path = load_csv_by_count(bcid_path, count)
        return send_file(path_or_file=bcid_path)
    elif stat_time:
        stat_path = os.path.join(PROJECT_PATH, "test_data", "send", stat_time + ".csv")
        if count:
            stat_path = load_csv_by_count(stat_path, count)
        return send_file(path_or_file=stat_path)
    else:
        file_1 = os.path.join(PROJECT_PATH, "test_data", "send", "id.csv")
        return send_file(path_or_file=file_1)


@app.route("/uploadFiles", methods=["GET"])
def upload_files():
    """ 模拟多个id
    不带参数为查询id目录
    带id为要下载id文件名
    """
    request_config = request.args.to_dict() or request.json or request.form.to_dict()
    id_name = request_config.get("id_name")
    ids_path = os.path.join(PROJECT_PATH, "test_data", "send", "ids")
    if not os.path.exists(ids_path):
        os.makedirs(ids_path)
    if not id_name:
        file_names = os.listdir(ids_path)
        return jsonify(data={"data": file_names})
    return send_from_directory(directory=ids_path, path=id_name)


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
    return jsonify({'code': 200, 'data': config})


@app.route("/batchCompute", methods=["POST"])
def batch_compute():
    send_path = os.path.join(PROJECT_PATH, "test_data", "send")
    check_path(send_path)
    file_name = "6666"
    config = {'taskIds': [file_name]}
    return jsonify({'code': 200, 'data': config})


@app.route("/online", methods=["POST"])
def data_on_line():
    dimension = 10
    config = request.json or request.args.to_dict() or request.form.to_dict()
    id_ = config.get("idValue")
    if not id_ or id_ not in LIMITED_ID:
        return jsonify({'code': 404, 'data': json.dumps({'response': {'tags': {}}})})
    result = {}
    for i in range(dimension):
        result['x{}'.format(i)] = str(random.random())

    return jsonify({'code': 200, 'data': json.dumps({'response': {'tags': result}})})


@app.route("/checkDownload", methods=["GET"])
def check_download():
    request_json = request.json or request.args.to_dict() or request.form.to_dict()
    bcid = request_json.get("bcId")
    if str(bcid) == "6666":
        bcid = "feature.csv"
    path = os.path.join(PROJECT_PATH, "test_data", "send", bcid)
    if os.path.exists(path):
        return jsonify({'code': 200})
    return jsonify({'code': 401})


def load_csv_by_count(path, count):
    if not count:
        raise ValueError("please set count")
    tmp_path = os.path.join(PROJECT_PATH, "test_data", "tmp")
    check_path(tmp_path)
    new_path = os.path.join(tmp_path, generate_tmp_table_name())
    df = pd.read_csv(path, header=0, dtype="str").iloc[0:int(count), :]
    columns = df.columns.values.tolist()
    df.to_csv(new_path, index=None, columns=columns)
    return new_path


def check_path(path):
    if not os.path.exists(path):
        os.makedirs(path)


if __name__ == "__main__":
    app.run(host=SERVING_HOST, port=PORT)
