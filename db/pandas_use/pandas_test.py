#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:  BryanGa
@time:  2022/01/06
@des:   
"""

import pandas as pd

train_data_path = "/Users/bryanga/PycharmProjects/self_test/db/source_data/trainData.csv"
test_data_path = "/Users/bryanga/PycharmProjects/self_test/db/source_data/testData.csv"


def get_head(start=101, end=201, y=None):
    if not y:
        head = ["id"] + ["x{}".format(str(i)) for i in range(start, end)]
    else:
        head = ["id", "y"] + ["x{}".format(str(i)) for i in range(start, end)]
    return head


if __name__ == "__main__":
    path = test_data_path
    path = train_data_path
    head_train_y = get_head(1, 101, 1)
    data_y = pd.read_csv(path, usecols=head_train_y)
    train_y_path = "/Users/bryanga/PycharmProjects/self_test/db/source_data/test_y.csv"
    train_y_path = "/Users/bryanga/PycharmProjects/self_test/db/source_data/train_y.csv"
    data_y.to_csv(train_y_path, columns=head_train_y, index=None)
    print("data_y 保存完成")
    head_train = get_head()
    data = pd.read_csv(path, usecols=head_train)
    train_path = "/Users/bryanga/PycharmProjects/self_test/db/source_data/test.csv"
    train_path = "/Users/bryanga/PycharmProjects/self_test/db/source_data/train.csv"
    data.to_csv(train_path, columns=head_train, index=None)
    print("data 保存完成")
