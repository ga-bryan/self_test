#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:  BryanGa
@time:  2022/02/08
@des:
给你两个 非空 的链表，表示两个非负的整数。它们每位数字都是按照 逆序 的方式存储的，并且每个节点只能存储 一位 数字。

请你将两个数相加，并以相同形式返回一个表示和的链表。

你可以假设除了数字 0 之外，这两个数都不会以 0 开头。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/add-two-numbers
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
"""


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def addTwoNumbers(self, l1: ListNode, l2: ListNode) -> ListNode:
        reustl = ListNode()
        while 1:
            number_1 = l1.next
            number_2 = l2.next
            add = 0
            add_1 = False
            # 当两个链表对应的位置都有数值时
            if number_1 and number_2:
                add = number_2 + number_1
                if add >= 10:
                    if add_1:
                        reustl.val = add - 9
                    else:
                        reustl.val = add - 10
                    add_1 = True
                else:
                    reustl.val = add
                reuslt = reustl.next


def reference(l1, l2):
    # 结果链表，当前指针
    result = curr = ListNode()
    # 进位项
    remainder = 0

    # 非空满足循环条件
    while l1 or l2:
        x = l1.val if l1 else 0
        y = l2.val if l2 else 0

        total = x + y + remainder

        curr.next = ListNode(total % 10)
        remainder = total // 10

        # 🚩防止某一链表已经为空，空链表.next会报错
        if l1: l1 = l1.next
        if l2: l2 = l2.next
        curr = curr.next

    if remainder: curr.next = ListNode(remainder)
    return result.next


if __name__ == "__main__":
    print(12 % 10)
    print(12 // 10)
