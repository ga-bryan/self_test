#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:  BryanGa
@time:  2021/11/30
@des:   临时
"""

import json
from random import sample
from datetime import datetime

pukes = {"z": "q", "x": "w", "c": "e", "v": "r"}
t = sample(list(pukes), 3)
print(t)

s = {"1": 1}
print(s.get(""))

print(datetime.fromisoformat("2021-12-01"))
