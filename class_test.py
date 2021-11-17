#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:  BryanGa
@time:  2021/11/09
@des:   类-学习
"""

import abc


class People(abc.ABC):
    """ 抽象类为所有类的基类，后续继承的类必须重新实现抽象类中定义的方法 """

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def info(self) -> str:
        return ""


class Person(People):

    def __init__(self, name, age, phone):
        super(Person, self).__init__(name, age)
        self.phone = phone

    def info(self):
        return "name: {}\n" \
               "age: {}\n" \
               "phone: {}\n".format(self.name, self.age, self.phone)


class Student(Person):
    def __init__(self, name, age, phone, school):
        super(Student, self).__init__(name, age, phone)
        self.school = school

    def info(self):
        return "name: {}\n" \
               "age: {}\n" \
               "phone: {}\n" \
               "school: {}".format(self.name, self.age, self.phone, self.school)


if __name__ == "__main__":
    p = Person("cjj", "25", "1111111")
    p_info = p.info()
    print(p_info)
    stu = Student("cjj", "25", "1111111", "岫岩高中")
    stu_info = stu.info()
    print(stu_info)
