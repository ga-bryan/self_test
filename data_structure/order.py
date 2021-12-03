#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:  BryanGa
@time:  2021/11/23
@des:   排序算法
"""


# 插入排序
def insert_sort(list_):
    length = len(list_)
    if length <= 1:
        return
    for i in range(1, length):
        value = list_[i]
        j = i - 1
        while 0 <= j < i:
            if list_[j] > value:
                list_[j + 1] = list_[j]
                j -= 1
            else:
                break
        list_[j + 1] = value


if __name__ == "__main__":
    list_ = [3, 4, 2, 5, 1, 7, 3]
    insert_sort(list_)
    print(list_)
