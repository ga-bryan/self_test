#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:  BryanGa
@time:  2021/08/20
@des:   线程试验
"""

import threading


class ThreadingTest(threading.Thread):
    def __init__(self, name):
        super(ThreadingTest, self).__init__()
        self.name = name

    def run(self):
        self.run_do()

    def run_do(self):
        while 1:
            print(self.name)




if __name__ == "__main__":
    ThreadingTest("cjj").start()
    # obj.start()
