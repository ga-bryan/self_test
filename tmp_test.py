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

download_url = "http://127.0.0.1:8182/api/batchCompute/resultDownload"
bcid = "665242146859540"
download_response = requests.get(download_url, params={"bcId": bcid})
response_json = download_response.json()
t = "s".encode()
s = "t"
path = "/Users/bryanga/PycharmProjects/self_test"
# zip_path = os.path.join(path, "a55c69e8a44caf74bbe6974c907cd9b6.zip")
# with ZipFile(zip_path, "r") as zFile:
#     for fileM in zFile.namelist():
#         zFile.extract(fileM, path=path, pwd=b'571efe7bb12eb97a')


import itertools
zip_path = os.path.join(path, "a55c69e8a44caf74bbe6974c907cd9b6.csv")
f = open(zip_path, "r", encoding="utf-8")
iters = itertools.cycle(f)
while 1:
    line = next(iters)
    print(line)



