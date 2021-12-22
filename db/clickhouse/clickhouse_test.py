#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:  BryanGa
@time:  2021/10/27
@des:   clickhouse数仓试验
"""

from click_house_setting import client

if __name__ == "__main__":
    table_name = "0aaaaaaa"
    # 删除表
    drop_table = "drop table dataaccess.{}".format(table_name)
    # client.execute(drop_table)

    # 创建表 `id2` String,
    create_sql = "CREATE TABLE if not exists dataaccess.{}(`id` String, `x0` String, `x1` String," \
                 " `x2` String, `x3` String) ENGINE = MergeTree order by tuple() primary key id, x0".format(table_name)
    create_result = client.execute(create_sql)

    # show_create = "show create table dataaccess.{}".format(table_name)
    # show_create_result = client.execute(create_sql)
    # print(show_create_result)

    # 插入数据
    insert_sql = "insert into dataaccess.{}(id,x0,x1,x2,x3) values " \
                 "(13762859944,0.9819446184100054,0.34655758432700423,0.7219176039918358,0.12708520041351234)".format(
        table_name)
    client.execute(insert_sql)

    # 查询数据
    select_sql = "select count(*) from dataaccess.{}".format(table_name)
    t = client.execute(select_sql)

    print(t)
    # 清空表
    truncate_sql = "truncate table dataaccess.{}".format(table_name)
    # client.execute(truncate_sql)
    # client.close()
