#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:  BryanGa
@time:  2021/12/22
@des:   单例模式的设计和实现
"""

import time
import threading
import os


class Singleton(object):
    _instance_lock = threading.Lock()
    _instance = {}

    def __init__(self):
        time.sleep(1)

    @classmethod
    def instance(cls, *args, **kwargs):
        with Singleton._instance_lock:
            if not hasattr(Singleton, "_instance"):
                Singleton._instance = Singleton(*args, **kwargs)
        return Singleton._instance


def singleton(cls, *args, **kw):
    """ 单例模式装饰器 """
    instances = {}

    def _singleton():
        key = str(cls) + str(os.getpid())
        if key not in instances:
            instances[key] = cls(*args, **kw)
        return instances[key]

    return _singleton


class IdCounter:
    """ 伴随线程安全的自增id """
    _lock = threading.RLock()

    def __init__(self, count=0):
        self._count = count

    def incr(self, delta=1):
        with IdCounter._lock:
            self._count += delta
            return self._count
