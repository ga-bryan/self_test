#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:  BryanGa
@des:   与文件有关的工具类方法
@time:  2021/07/07
"""

import os
from functools import lru_cache
from typing import Mapping

import yaml
import pandas as pd
from utils.path_utils import get_project_base_directory


def _merge_dictionaries(a, b):
    """
    合并同一个key
    :param a:
    :param b:
    :return:
    """
    merged = a.copy()
    for key in b:
        if key in a:
            if isinstance(a[key], Mapping) and isinstance(b[key], Mapping):
                merged[key] = _merge_dictionaries(a[key], b[key])
            else:
                merged[key] = b[key]
        else:
            merged[key] = b[key]
    return merged


@lru_cache()
def load_yaml_conf(_conf_path=None):
    """
    加载并处理yaml文件内容
    :param _conf_path:
    :return:
    """
    if not _conf_path:
        _conf_path = os.path.join(get_project_base_directory(), "config.yaml")
    try:
        cfg = {}
        with open(_conf_path) as f:
            values = yaml.safe_load(f)
        if isinstance(values, dict):
            cfg = _merge_dictionaries(cfg, values)
        return cfg
    except Exception as e:
        raise EnvironmentError(
            "loading yaml file config from {} failed:".format(_conf_path), e
        )


def _get_yaml(*keys):
    """
    加载yaml文件
    :param keys:
    :return:
    """
    configs = load_yaml_conf()
    for key in keys:
        configs = configs.get(key, None)
        if configs is None:
            break
    return configs


def get_conf(key, default=None):
    """
    按key读取保存在yaml中的内容
    :param key:
    :param default:
    :return:
    """
    # Environment variables have higher priority than configuration file.
    result = os.environ.get(key, None)
    if result is None:
        result = _get_yaml(*[i.lower() for i in key.split("_")])
    if result is None:
        result = default
    return result


def read_file_by_batch(file_path):
    """
    按照指定大小批次处理一个文件
    :param file_path:
    :return:
    """

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
