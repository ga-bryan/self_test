#!/usr/bin/python
# -*- coding: UTF-8 -*
"""
@author: gaoxiaolong
@time: 2022/1/17
"""

import json
import os
import time
from zipfile import ZipFile

import pandas as pd
import requests

from db.models import DmsJob
from operater.common_operate import FEATURES_PATH
from operater.umeng_config import ALL_HEADERS
from utils.constant_utils import JobType
from utils.core_utils import pretty
from utils.file_utils import check_path, get_project_base_directory, remove_tmp_file
from utils.job_utils import generate_table_name, job_callback, return_status_msg
from utils.log_utils import dete_logger, job_logger
from utils.minio_utils import put_object
from utils.setting import (
    COMMENTS,
    DATA_SET_IDTYPE,
    DATA_SET_NAME,
    DATA_SET_TYPE,
    TASK_NAME,
    UMENG_BATCH_COMPUTE_URL,
    UMENG_DOWNLOAD_URL,
    UMENG_ONLINE_URL,
)


def export_offline_data(job_id, request_info):
    data_url = request_info.get("data_url", None)
    if not data_url:
        raise ValueError("please config data_url")
    job_path = os.path.join(get_project_base_directory(), "tmp", job_id)
    check_path(job_path)
    # 下载求交数据
    response = requests.get(data_url)
    if response.content:
        intersection_path = os.path.join(
            job_path, generate_table_name(job_id, str(time.time())) + ".csv"
        )
        open(intersection_path, "wb").write(response.content)
        if not (
                request_info.get("stat_times")
                and isinstance(request_info.get("stat_times"), list)
        ):
            raise ValueError("please set stat_times and set stat_times rightly")
        intersection_paths = add_time(intersection_path, request_info.get("stat_times"))
        taskIds = []
        for intersection_path in intersection_paths:
            batch_compute_json = build_batch_compute_json(
                intersection_path,
                DATA_SET_NAME,
                DATA_SET_TYPE,
                DATA_SET_IDTYPE,
                TASK_NAME,
                COMMENTS,
            )
            resp = requests.post(url=UMENG_BATCH_COMPUTE_URL, json=batch_compute_json)
            remove_tmp_file(intersection_path)
            data = resp.json().get("data")
            if not data:
                return return_status_msg(data=resp.text)
            task_ids = data.get("taskIds")
            if task_ids:
                taskIds.extend(task_ids)
        if taskIds:
            bcids = ",".join([str(i) for i in taskIds])
            request_info["bcids"] = bcids
            DmsJob.create_job(
                job_id,
                JobType.UMENG_OFFLINE.value,
                request_info,
            )
            job_logger(job_id).info(
                'save job {} info {}'.format(job_id, pretty(request_info))
            )

    return return_status_msg()


def export_offline4_predict(job_id, request_info):
    data_url = request_info.get("data_url", None)
    callback_url = request_info.get("callback_url", None)
    callback_data = None
    if not data_url:
        raise ValueError("please config data_url url")
    request_info["reqId"] = job_id
    # 下载求交id结果
    job_path = os.path.join(get_project_base_directory(), "tmp", job_id)
    check_path(job_path)
    intersection_path = os.path.join(
        job_path, generate_table_name(job_id, str(time.time())) + ".csv"
    )
    download_by_url(data_url, intersection_path)

    result = {"values": []}
    idType = request_info.get("idType")
    with open(intersection_path, "r") as f:
        while 1:
            line = f.readline()
            if not line.strip():
                break
            id_value = line.strip()
            request_info = build_request_json(id_value, idType)
            response = requests.post(UMENG_ONLINE_URL, json=request_info)
            data = get_content(response)
            if data:
                if not result.get("columns"):
                    result["columns"] = list(data.keys())
                result["values"].append(list(data.values()))
    remove_tmp_file(intersection_path)
    if result.get("values"):
        file_name = generate_table_name(job_id, str(time.time())) + ".csv"
        path = os.path.join(job_path, file_name)
        pd.DataFrame(result.get("values"), columns=result.get("columns")).to_csv(
            path, index=None
        )
        minio_url = put_object(file_name, path)
        callback_data = {
            'status': 0,
            'msg': "success",
            'data': {"minio_files": [minio_url]},
            "job_id": job_id,
        }
        DmsJob.update_job(job_id, result=callback_data)
        if callback_url:
            job_callback(job_id, callback_url, callback_data)
        remove_tmp_file(path)
    DmsJob.succeed_job(job_id)
    job_logger(job_id).info("job succeed")
    return return_status_msg(data=callback_data)


def request_online_data(umeng_info):
    response = requests.post(UMENG_ONLINE_URL, json=umeng_info)
    # todo：code返回值的处理
    data = get_content(response)
    if data:
        return return_status_msg(status=200, data=data)
    return return_status_msg(status=404)


def get_content(response):
    if response.json().get("code") == 200:
        response_json = response.json()
        # todo：根据实际路径调整，现阶段中转方式多层封装
        data = json.loads(response_json.get("data"))
        if data.get("response").get("tags"):
            return data.get("response").get("tags")
    return None


def build_request_json(idValue, idType):
    return {"idValue": idValue, "idType": idType}


def build_batch_compute_json(
        localCsvFile, dataSetName, dataSetType, dataSetIdType, taskName, comments
):
    return {
        "localCsvFile": localCsvFile,
        "dataSetName": dataSetName,
        "dataSetType": dataSetType,
        "dataSetIdType": dataSetIdType,
        "taskName": taskName,
        "comments": comments,
    }


def download_by_url(url, path):
    content = requests.get(url).content
    open(path, "wb").write(content)
    return True


def check_if_download_success(bcids, download_url):
    bcids = bcids.split(",")
    for bcid in bcids:
        response = requests.get(download_url, params={"bcId": bcid})
        dete_logger.info(
            "dete bcids:{},resp_code:{}".format(bcids, response.json().get("code"))
        )
        if response.json().get("code") != 200:
            return False
    # todo：增加保存数据动作，后由commom统一执行数据上传
    return True


def add_time(csv_path, stat_times, chunksize=10000):
    """id求交文件补充回溯时间"""
    result = []
    for stat_time in stat_times:
        new_csv_path = os.path.join(
            get_project_base_directory(),
            "tmp",
            generate_table_name(str(time.time()), str(time.time())) + ".csv",
        )
        header = pd.read_csv(csv_path, header=0).columns.values.tolist()
        chunks = pd.read_csv(csv_path, chunksize=chunksize, usecols=header)

        stat_times = [[stat_time] for i in range(chunksize)]
        for index, chunk in enumerate(chunks):
            if index == 0:
                pd.concat(
                    [
                        chunk.reset_index(drop=True),
                        pd.DataFrame(
                            [["date"]]
                            + [[stat_time] for i in range(chunk.shape[0] - 1)]
                        ),
                    ],
                    axis=1,
                ).to_csv(new_csv_path, mode="a", index=None, header=None)
            elif chunk.shape[0] < chunksize:
                pd.concat(
                    [
                        chunk.reset_index(drop=True),
                        pd.DataFrame([[stat_time] for i in range(chunk.shape[0])]),
                    ],
                    axis=1,
                ).to_csv(new_csv_path, mode="a", index=None, header=None)
            else:
                pd.concat(
                    [chunk.reset_index(drop=True), pd.DataFrame(stat_times)], axis=1
                ).to_csv(new_csv_path, mode="a", index=None, header=None)
        result.append(new_csv_path)
    return result


def reset_id(csv_path, chunksize=10000, new_csv_path=None):
    """重置id为 id#回溯时间"""
    chunks = pd.read_csv(csv_path, chunksize=chunksize, header=0, dtype="str")
    header = pd.read_csv(csv_path, header=0).columns.values.tolist()
    if not new_csv_path:
        new_csv_path = os.path.join(
            get_project_base_directory(),
            "tmp",
            generate_table_name(str(time.time()), str(time.time())) + ".csv",
        )
    for index, chunk in enumerate(chunks):
        # 第二列必须是时间
        chunk[header[0]] = chunk[header[0]] + "#" + chunk[header[1]]
        if index == 0:
            new_header = header[0:1]
            new_header.extend(header[2:])
            chunk.to_csv(
                new_csv_path, mode="a", index=None, header=True, columns=new_header
            )
        else:

            chunk = pd.concat([chunk.iloc[:, 0], chunk.iloc[:, 2:]], axis=1)
            chunk.to_csv(new_csv_path, mode="a", header=None, index=None)

    return new_csv_path


def get_features(file_path):
    # todo：更新友盟特征提取
    if not os.path.exists(file_path):
        return
    new_csv_path = os.path.join(
        get_project_base_directory(),
        "tmp",
        generate_table_name(str(time.time()), str(time.time())) + ".csv",
    )
    template = pd.DataFrame([], columns=["id"] + ALL_HEADERS)
    template.to_csv(new_csv_path, header=True, index=False)
    count = 0
    with open(file_path, "r") as f:
        f.readline()
        while 1:
            line = f.readline().strip()
            if not line:
                break
            cells = line.split(",")
            value = ["{}#{}".format(cells[0], cells[2])]
            header = ["id"]
            for dict_ in cells[6].split(" "):
                columns = dict_.split(":")
                header.append(columns[0])
                value.append(columns[-1])
            df = pd.concat(
                [template, pd.DataFrame([value], columns=header)], join="outer"
            )
            df.fillna(-9999, inplace=True)
            df.to_csv(new_csv_path, mode="a", index=False, header=False)
            count += 1
            if count % 1000 == 0:
                print("---- has been get {} data -----".format(count))
    return new_csv_path


def mutlti_process_data(lines: list):
    template = pd.DataFrame([], columns=["id"] + ALL_HEADERS)
    result = []
    for line in lines:
        line = line.strip()
        cells = line.split(",")
        value = ["{}#{}".format(cells[0], cells[2])]
        header = ["id"]
        for dict_ in cells[6].split(" "):
            columns = dict_.split(":")
            header.append(columns[0])
            value.append(columns[-1])
        df = pd.concat([template, pd.DataFrame([value], columns=header)], join="outer")
        df.fillna(-9999, inplace=True)
        result.append(df.values.tolist())
    return result


def download_data(job_id, download_info):
    """ 友盟数据下载 """
    bcids = download_info.get("bcids")
    if not bcids:
        return return_status_msg()
    catalogue = download_info.get("catalogue")
    job_path = os.path.join(FEATURES_PATH, catalogue)
    tmp_path = os.path.join(get_project_base_directory(), "tmp", job_id)
    check_path(job_path)
    for bcid in bcids.split(","):
        response = requests.get(UMENG_DOWNLOAD_URL, params={"bcId": bcid})
        file_name = generate_table_name(job_id, str(time.time())) + ".csv"
        csv_path = os.path.join(tmp_path, file_name)
        open(csv_path, "wb").write(response.content)
        file_path = os.path.join(job_path, file_name)
        # todo：按照友盟最新的约定处理下载文件
        path = reset_id(tmp_path, file_path)
    open(os.path.join(FEATURES_PATH, catalogue, "finished"), "w").write("")


def download_data_real(job_id, download_info):
    job_path = os.path.join(get_project_base_directory(), "tmp", job_id, "zipFiles")
    check_path(job_path)
    bcids = download_info.get("bcids")
    callback_url = download_info.get("callback_url", None)
    result = {"minio_files": []}
    callback_data = None
    if not bcids:
        return None
    if bcids:
        bcids = bcids.split(",")
        for bcid in bcids:
            response = requests.get(UMENG_DOWNLOAD_URL, params={"bcId": bcid})
            data = response.json().get("data")
            export_file_name = data.get("exportFileName")
            password = data.get("password").encode()
            zip_path = os.path.join(
                job_path, generate_table_name(job_id, str(time.time())) + ".zip"
            )
            download_by_url(export_file_name, zip_path)
            with ZipFile(zip_path) as down_zip:
                for file_name in down_zip.namelist():
                    path = os.path.join(job_path, file_name)
                    down_zip.extract(file_name, path=job_path, pwd=password)
                    minio_url = put_object(file_name, path)
                    # todo：导出的id为"id#回溯时间"
                    result["minio_files"].append(minio_url)
                    remove_tmp_file(path)
        callback_data = {
            'status': 0,
            'msg': "success",
            'data': result,
            "job_id": job_id,
        }
        DmsJob.update_job(job_id, result=callback_data)
        if callback_url:
            job_callback(job_id, callback_url, callback_data)
        remove_tmp_file(zip_path)
    DmsJob.succeed_job(job_id)
    job_logger(job_id).info("job succeed")
    return return_status_msg(data=callback_data)


if __name__ == "__main__":
    start_time = time.time()
    csv_path = "/Users/bryanga/PycharmProjects/self_test/test_data/tmp/feature.csv"
    t = "/Users/bryanga/PycharmProjects/dataaccess/tmp/ttt.csv"
    print(pd.read_csv(t).values.tolist())
    # print(get_features(csv_path))
    # print(time.time() - start_time)
