#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:  BryanGa
@time:  2021/12/28
@des:
"""
import os
from functools import lru_cache
from typing import Mapping

import yaml

_conf_path = os.path.join(get_project_base_directory(), "config.yaml")


def _get_yaml(*keys):
    configs = load_yaml_conf()
    for key in keys:
        configs = configs.get(key, None)
        if configs is None:
            break
    return configs


def get_conf(key, default=None):
    # Environment variables have higher priority than configuration file.
    result = os.environ.get(key, None)
    if result is None:
        result = _get_yaml(*[i.lower() for i in key.split("_")])
    if result is None:
        result = default
    return result


@lru_cache()
def load_yaml_conf():
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


def _merge_dictionaries(a, b):
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
