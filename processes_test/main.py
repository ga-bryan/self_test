#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:  BryanGa
@time:  2022/04/12
@des:   
"""
import time
from multiprocessing import Pool, cpu_count, Process, Queue, Event

QUEUE = [Queue(10) for i in range(5)]

event = Event()


def add_task(queue):
    while 1:
        for i in range(10):
            queue.put(i)
        # time.sleep(4)
        # event.wait(4)
    # for i in range(10):
    #     queue.put(i)
    # time.sleep(4)


def worker(queue):
    while 1:
        # value = queue.get("1234")
        value = queue.get()
        print("---{}____".format(queue.qsize))
        if not value:
            print("当前没有待处理任务")
            time.sleep(5)
        print("----{}----".format(value))


if __name__ == "__main__":
    # producer = Process(target=add_task, args=(QUEUE[0],), daemon=True)
    # # for i in range(10):
    # #     QUEUE[0].put(i)
    # consumer = Process(target=worker, args=(QUEUE[0],), daemon=True)
    # consumer.start()
    # producer.start()
    # consumer.join()
    # producer.join()
    # print("---hhh----")
    add_task(QUEUE[0])
    # at()
