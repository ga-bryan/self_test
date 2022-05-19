#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:  BryanGa
@time:  2022/03/15
@des:   辅助个推数据源的添加
"""

import os
import pandas as pd
from setting import PROJECT_PATH


def load_brands(brand_path=None):
    result = {"luxury": [], "normal": [],
              "other": []}
    if not brand_path:
        brand_path = os.path.join(
            PROJECT_PATH, "operater", "01 4s店品牌_2.csv"
        )
    brands = pd.read_csv(brand_path, usecols=["汽车品牌", "最终结果"], encoding="gbk").values.tolist()
    for line in brands:
        if line[-1] == "豪华":
            result["luxury"].append(line[0])
        elif line[-1] == "其他":
            result["other"].append(line[0])
        else:
            result["normal"].append(line[-1])
    print(result)


def load_label():
    path = "/Users/bryanga/PycharmProjects/self_test/assist_work/gt/03 联邦学习特征梳理_更新频率_v1.0_20220316.xlsx"
    labels = pd.read_excel(path, sheet_name="特征v1.1-v1.2", usecols=["特征介绍"]).values.tolist()
    labels_series = []
    for line in labels:
        s = line[0].split("：")
        if len(s) > 1:
            labels_series.append(s[-1].strip())
    print(labels_series)


if __name__ == "__main__":
    # load_brands("/Users/bryanga/PycharmProjects/self_test/assist_work/gt/01 4s店品牌_2.csv")
    load_label()
