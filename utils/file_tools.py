#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:  BryanGa
@des:   与文件有关的工具类方法
@time:  2021/07/07
"""

import os

import yaml
import pandas as pd


def get_project_base_path():
    return os.path.abspath(os.path.join(__file__, "../.."))


def load_yaml(yaml_path):
    with open(yaml_path) as f:
        values = yaml.safe_load(yaml_path, Loader=yaml.FullLoader)


def read_file_by_batch(file_path):
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
    print(get_project_base_path())
