#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:  BryanGa
@time:  2022/04/06
@des:   启动进程
"""

import os
from multiprocessing import Lock, Pool, Process, Queue, freeze_support
from os import cpu_count

import pandas as pd

from operater.test import add_task, multiprocess_creat, q_1
from utils.setting import ALL_HEADERS

_lock = Lock()

# count of processes
NUMBER_OF_PROCESSES = os.cpu_count() - 1


# def mutlti_process_data_do(lines: list):
#     print("--- start to mutlti_process_data_do ---")
#     if not lines:
#         return None
#     template = pd.DataFrame([], columns=["id"] + ALL_HEADERS)
#     for line in lines:
#         line = line.strip()
#         cells = line.split(",")
#         value = ["{}#{}".format(cells[0], cells[2])]
#         header = ["id"]
#         for dict_ in cells[6].split(" "):
#             columns = dict_.split(":")
#             header.append(columns[0])
#             value.append(columns[-1])
#         template = pd.concat(
#             [template, pd.DataFrame([value], columns=header)], join="outer"
#         )
#     return template
def mutlti_process_data_do(s):
    print("--- start to mutlti_process_data_do ---")
    return "ssss"


def submit_task(queue_, data):
    for i in range(len(data)):
        queue_.put(data[i])
        # queue_.put("ssssss")
    queue_.put(None)


def start_worker(queue_):
    p = Pool(cpu_count() - 1)
    for i in range(len(queue_)):
        lines = queue_.get()
        p.apply_async(mutlti_process_data_do, args=(lines,))
    p.close()
    p.join()


def get_result(queue_, result_path):
    for i in range(len(queue_)):
        df = queue_.get()
        if not df:
            return
        df.fillna(-9999, inplace=True)
        df.to_csv(result_path, header=False, index=False, mode="a")


def mutlti_process_data(file_path, result_path):
    print("--- start to mutlti_process_data ---")
    template = pd.DataFrame([], columns=["id"] + ALL_HEADERS)
    template.to_csv(result_path, header=True, index=False, mode="a")
    count = 0
    batch = []
    process_list = []
    process_size = 0
    with open(file_path, "r") as f:
        f.readline()
        while 1:
            line = f.readline().strip()
            if not line:
                break
            # batch.append(line)
            count += 1
            process_size += 1
            process_list.append(line)
            if process_size == 10:
                batch.append(process_list[:])
                process_list.clear()
                process_size = 0
            if count == process_size * cpu_count():
                queue_ = Queue(cpu_count() - 1)
                submit_task(queue_, batch[:])
                start_worker(queue_)
                get_result(queue_, result_path)
                batch.clear()
                count = 0
    if process_list or batch:
        batch.append(process_list)
        queue_ = Queue(cpu_count() - 1)
        print("---queue_----")
        submit_task(queue_, batch)
        print("---submit_task---")
        start_worker(queue_)
        print("----start_worker----")
        get_result(queue_, result_path)
    cjj = ""


if __name__ == '__main__':
    # freeze_support()
    # path = "/Users/bryanga/PycharmProjects/dataaccess/tmp/20220406_1638181/dms_41cc2894bb40306cb159de06c0835f3d.csv"
    # result_path = "/Users/bryanga/PycharmProjects/dataaccess/data/features/cjj.csv"
    # if os.path.exists(result_path):
    #     os.remove(result_path)
    # mutlti_process_data(path, result_path)
    add_task(q_1)
    multiprocess_creat(q_1)
