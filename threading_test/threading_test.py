#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:  BryanGa
@time:  2021/08/20
@des:   线程试验
"""

import threading

"""

    run(): 用以表示线程活动的方法。
    start():启动线程活动。

    join([time]): 等待至线程中止。这阻塞调用线程直至线程的join() 方法被调用中止-正常退出或者抛出未处理的异常-或者是可选的超时发生。
    isAlive(): 返回线程是否活动的。
    getName(): 返回线程名。
    setName(): 设置线程名。

"""


class ThreadingTest(threading.Thread):
    count = 0

    def __init__(self, name):
        super(ThreadingTest, self).__init__()
        self.name = name

    def run(self):
        """ 如果这个函数需要操纵全局变量，需要加锁 """
        threading.Lock.acquire()  # 获取锁
        self.run_do()
        threading.Lock.release()  # 释放锁

    def run_do(self):
        self.count += 1
        print("当前的线程名称是: {}\n当前的线程的count值为：{}".format(self.name, self.count))
        return self.count


if __name__ == "__main__":
    thread1 = ThreadingTest("cjj")
    thread2 = ThreadingTest("xxx")
    thread1.start()
    thread2.start()
    # 等待所有线程结束后再退出主线程，可以不等
    thread1.join()
    thread2.join()
    print("退出主线程")
