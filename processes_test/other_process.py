#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:  BryanGa
@time:  2022/04/12
@des:   
"""

from processes_test.main import QUEUE

if __name__ == "__main__":
    for i in range(10):
        QUEUE[0].put(i)
    print(QUEUE[0].qsize())
