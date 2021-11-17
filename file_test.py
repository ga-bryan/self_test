#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:  BryanGa
@time:  2021/11/09
@des:   文件相关的操作
"""
import time
import os.path

import pandas as pd
from setting import DATA_PATH

file_path = os.path.join(DATA_PATH, "user_log_format1.csv")
header = ['user_id', 'item_id', 'cat_id', 'seller_id', 'brand_id', 'time_stamp', 'action_type']


def read_file_by_batch():
    def deal_chunk(x):
        return x

    results = []
    chunk_iterators = pd.read_csv(file_path, chunksize=10000)  # 每次读指定数量的行
    for chunk_iterator in chunk_iterators:
        # todo:deal data function
        filter_result = deal_chunk(chunk_iterator)
        results.append(filter_result)
    df = pd.concat(results)
    return df


if __name__ == "__main__":
    a = int(" 12  ")
    start_time = time.time()
    df = read_file_by_batch()
    print(time.time() - start_time)
