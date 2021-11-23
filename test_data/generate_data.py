#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:  BryanGa
@time:  2021/10/22
@des:   
"""

import random
import pandas as pd
import os
from loguru import logger
import time

logger.add("log.log")

root_path = os.path.dirname(os.path.abspath(__file__))

dimension = 200
columns = [["id"] + ["x{}".format(i) for i in range(dimension)]]


def random_phone():
    prelist = ["130", "131", "132", "133", "134", "135", "136", "137", "138", "139", "147", "150", "151", "152",
               "153", "155", "156", "157", "158", "159", "186", "187", "188"]
    return random.choice(prelist) + "".join(random.choice("0123456789") for i in range(8))


if __name__ == "__main__":
    start_time = time.time()
    for num in range(1, 11):
        file_name = str(num) + ".csv"
        path = os.path.join(root_path, file_name)
        if os.path.exists(path):
            logger.info("覆盖同名文件: {}".format(file_name))
        logger.info("开始保存文件： {}".format(path))
        pd.DataFrame(columns).to_csv(path, header=0, index=False)
        batch_size = 0
        data_count = 0
        result = []
        for id in range(num * 100000):
            batch_size += 1
            result.append([random_phone()] + [random.random() for i in range(dimension)])
            if batch_size == 10000:
                pd.DataFrame(result).to_csv(path, index=False, mode="a", header=False)
                result.clear()
                data_count += batch_size
                logger.info("完成 {} 条".format(data_count))
                batch_size = 0
        if result:
            pd.DataFrame(result).to_csv(path, header=False, index=False, mode="a")
        logger.info("保存当前文件 {} 用时 {} ".format(file_name, time.time() - start_time))
    print("总用时 {}".format(time.time() - start_time))
