#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:  BryanGa
@time:  2022/01/13
@des:   
"""

import threading
import random
from random import shuffle, sample


class FraudulentGoldFlower:
    _instance_lock = threading.Lock()
    puke_backup = {}  # 完整的扑克牌
    pukes = {}  # 完整的扑克牌

    def __init__(self):
        self.puke_backup = self.get_pks()
        self.pukes = self.shuffle()

    @classmethod
    def get_pks(cls):
        """
        生成完整的扑克
        :return:
        """

        colors = ["黑桃", "红心", "方块", "梅花"]
        numbers = [str(i) for i in range(2, 11)] + ["J", "Q", "K", "A"]
        pks = {}  # 所有的扑克牌
        for color in colors:
            value = 2
            for num in numbers:
                pks["{} {}".format(color, num)] = value
                value += 1
        return pks

    @classmethod
    def shuffle(cls):  # 洗牌
        keys = list(cls.puke_backup.keys())
        random.shuffle(keys)
        pkes = {}
        for key in keys:
            pkes[key] = cls.puke_backup[key]
        return pkes

    def send_pk(self):
        """
        发牌
        :return:
        """
        with self._instance_lock:
            result = {}
            if len(self.pukes) < 3:
                return {"mesaage": "此轮结束，再次请求开始下一轮"}
            pk = sample(list(self.pukes), 3)
            for index, _pk in enumerate(pk):
                result.update({str(index): _pk})
                del self.pukes[_pk]
            print(len(self.pukes.keys()))
            return result

    @classmethod
    def show_pukes(cls, pks):
        """
        查看手中的扑克
        :param pks:
        :return:
        """
        return

    def restart(self):
        self.pukes.clear()
        self.pukes = self.shuffle()
