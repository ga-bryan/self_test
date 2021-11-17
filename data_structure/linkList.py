#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:  BryanGa
@time:  2021/10/25
@des:   链表
"""


class Node:
    def __init__(self, value=None, next=None):
        self.value = value
        self.next = next


class SingleNode:
    def __init__(self):
        self.head = Node()

    def InitListNode(self, data: list):
        self.head = Node(data[0])
        p = self.head
        for d in data[1:]:
            p.next = Node(d)
            p = p.next

    def empty(self):
        if not self.head:
            print("ListLinkNode is empty")
            return True
        else:
            return False

    def get_length(self):
        if self.empty():
            return 0
        count = 0
        while p:
            count += 1
            p = p.next
        return count

    def print(self):
        p = self.head
        while p:
            print(p.value)
            p = p.next

    def get_data_by_index(self, index):
        if index > self.get_length():
            return -1
        p = self.head
        count = 1
        while p:
            if count == index:
                return p.next.value
            count += 1
            p = p.next


def find():
    """

    :return:
    """


if __name__ == "__main__":
    lnode = SingleNode()

