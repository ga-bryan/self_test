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
from utils.file_tools import get_project_base_path

data_path = os.path.join(get_project_base_path(), "test_data", "ten_million.csv")

columns = ["id", "x0", "x1", "x2", "x3"]

result = [columns]


def random_phone():
    prelist = ["130", "131", "132", "133", "134", "135", "136", "137", "138", "139", "147", "150", "151", "152",
               "153", "155", "156", "157", "158", "159", "186", "187", "188"]
    return random.choice(prelist) + "".join(random.choice("0123456789") for i in range(8))


for id in range(10000000):
    result.append([random_phone(), random.random(), random.random(), random.random(), random.random()])

pd.DataFrame(result).to_csv(data_path, header=0, index=False)
