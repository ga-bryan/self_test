#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:  BryanGa
@time:  2021/10/27
@des:   clickhouse数仓试验
"""

from click_house_setting import client, db

if __name__ == "__main__":
    table_name = "bryanga_test"
    # 删除表
    drop_table = "drop table {}.{}".format(db, table_name)
    # client.execute(drop_table)

    # 创建表 `id2` String,
    create_sql = "CREATE TABLE if not exists {}.{}(史蒂夫 String, `x0` String, `x1` String," \
                 " `x2` String, `x3` String) ENGINE = MergeTree order by id".format(db,
                                                                                                            table_name)
    create_result = client.execute(create_sql)

    # show_create = "show create table dataaccess.{}".format(table_name)
    # show_create_result = client.execute(create_sql)
    # print(show_create_result)

    # 插入数据
    insert_sql = "insert into {}.{}(id,x0,x1,x2,x3) values " \
                 "(13762859944,0.9819446184100054,0.34655758432700423,0.7219176039918358,0.12708520041351234)".format(
        db, table_name)
    # client.execute(insert_sql)

    # 查询数据
    # select_sql = "select count(1) from {}.{}".format(db, table_name)
    select_sql = "select count(1) from {}".format("(select * from {})".format(table_name))
    print(select_sql)
    t = client.execute(select_sql)[0][0]

    print(t)
    # 清空表
    truncate_sql = "truncate table {}.{}".format(db, table_name)
    # client.execute(truncate_sql)
