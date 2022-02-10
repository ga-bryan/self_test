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
import requests
from zipfile import ZipFile
import os

pukes = {"z": "q", "x": "w", "c": "e", "v": "r"}
t = sample(list(pukes), 3)
print(t)

s = {"1": 1}
print(s.get(""))

print(datetime.fromisoformat("2021-12-01"))

dict_ = {"t": 1}
print(list(dict_.keys()))

# download_url = "http://127.0.0.1:8182/api/batchCompute/resultDownload"
# bcid = "665242146859540"
# download_response = requests.get(download_url, params={"bcId": bcid})
# response_json = download_response.json()

tmp_path = "/Users/bryanga/PycharmProjects/self_test/tmp.json"

t = ["t"]
open(tmp_path, "w").write(json.dumps(t))


