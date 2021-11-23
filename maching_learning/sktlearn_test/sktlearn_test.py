#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:  BryanGa
@time:  2021/07/12
@des:   sktlearn 练习
"""

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
import sklearn


def _get_model_message(y_true, y_predicted):
    from sklearn.metrics import accuracy_score, recall_score, f1_score, confusion_matrix, precision_score
    acc = accuracy_score(y_true, y_predicted, normalize=False)
    pre = precision_score(y_true, y_predicted, average="micro")
    recall = recall_score(y_true, y_predicted, average="micro")
    f1 = f1_score(y_true, y_predicted, average="weighted")
    confusion_matrix_ = confusion_matrix(y_true, y_predicted)
    return acc, pre, recall, f1, confusion_matrix_


x_train = np.array([[1, 2, 3],
                    [1, 3, 4],
                    [2, 1, 2],
                    [4, 5, 6],
                    [3, 5, 3],
                    [1, 7, 2]])

y_train = np.array([3, 3, 3, 2, 2, 2])

x_test = np.array([[2, 2, 2],
                   [3, 2, 6],
                   [1, 7, 4]])

clf = LogisticRegression()
clf.fit(x_train, y_train)

# 返回预测标签
result_tag = clf.predict(x_train)
print(result_tag)
result_tag = pd.DataFrame(result_tag, columns=[1])
y_train = pd.DataFrame(y_train, columns=[1])
acc, pre, recall, f1, confusion_matrix_ = _get_model_message(y_train[1], result_tag[1])
print(acc)
print(pre)
print(recall)
print(f1)
print(confusion_matrix_)

# 返回预测属于某标签的几率
# print(clf.predict_proba(x_test))
