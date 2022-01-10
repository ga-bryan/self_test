#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:  BryanGa
@time:  2021/12/28
@des:   
"""

import base64
import uuid
import threading
import time


def string_to_byte(string_):
    return base64.b64encode(string_.encode("utf-8"))


def byte_to_string(bytes):
    return bytes.decode(encoding="utf-8")


def base64_encode(string_):
    return byte_to_string(string_to_byte(string_))


class IdCounter:
    _lock = threading.RLock()

    def __init__(self, counter=0):
        self._count = counter

    @property
    def incr(self, step=1):
        with self._lock:
            self._count += step
            return self._count


id_counter = IdCounter()


def generate_tmp_table_name():
    return "{}.csv".format(
        uuid.uuid3(
            uuid.NAMESPACE_DNS,
            base64_encode(str(id_counter.incr) + str(time.time()))
        )
    )


if __name__ == "__main__":
    print(base64_encode("tttt1111"))
