#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:  BryanGa
@time:  2022/01/05
@des:   
"""

import pymysql

db = pymysql.connect(host='172.16.0.157',
                     user='dppc',
                     password='dppc',
                     database='dppc',
                     port=31447)
cursor = db.cursor()


def create_table(table_name, start=101, end=201, y=None):
    if y:
        sql = "CREATE TABLE IF NOT EXISTS `t_{}` (`id` int,`y` int,{},PRIMARY KEY ( `id` ));".format(
            table_name, ",".join(["`x" + str(i) + "`" + " float" for i in range(start, end)]))
    else:
        sql = "CREATE TABLE IF NOT EXISTS `t_{}` (`id` int,`y` int,{},PRIMARY KEY ( `id` ));".format(
            table_name, ",".join(["`x" + str(i) + "`" + " float" for i in range(start, end)]))
    cursor.execute(sql)


def insert(table_name, head, generate):
    sql = "insert into {}({}) values ".format(table_name, head)
    batch_size = 0
    batch = []
    count = 0
    for line in generate:
        # t = line.split(",")
        batch.append("(" + line + ")")
        batch_size += 1
        if batch_size == 1000:
            insert_sql = sql + ",".join(batch) + ";"
            cursor.execute(insert_sql)
            db.commit()
            batch_size = 0
            batch.clear()
            count += 1000
            print("has been inserted {}".format(count))
    if batch:
        insert_sql = sql + "(" + ",".join(batch) + ")"
        cursor.execute(insert_sql)
        db.commit()
        count += batch_size
        print("has been insered {}".format(count))


def load_data(csv_path, y=None):
    head = True
    with open(csv_path, "r") as f:
        while 1:
            line = f.readline()
            if head:
                head = False
                continue
            tmp_line = line.split(",")
            if y:
                line = ",".join(line.split(",")[:102]).strip()
            else:
                line = ",".join(tmp_line[0:1] + tmp_line[102:]).strip()
            yield line


def get_head(start=101, end=201, y=None):
    if not y:
        head = ["`id`"] + ["`x{}`".format(str(i)) for i in range(start, end)]
    else:
        head = ["`id`", "`y`"] + ["`x{}`".format(str(i)) for i in range(start, end)]
    return ",".join(head)


if __name__ == "__main__":
    # 生成带y特征表
    create_table("train_y", start=1, end=101)
    test_data_path = "/Users/bryanga/PycharmProjects/self_test/db/source_data/testData.csv"
    generate_y = load_data(test_data_path, y=True)
    head_y = get_head(start=1, end=101, y=1)
    insert("t_train_y", head_y, generate_y)
    # 生成非y特征表
    create_table("train")
    train_data_path = "/Users/bryanga/PycharmProjects/self_test/db/source_data/trainData.csv"
    generate = load_data(train_data_path)
    head = get_head(start=101, end=201)
    insert("t_train", head, generate)
