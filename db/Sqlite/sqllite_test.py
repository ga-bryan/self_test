#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:  BryanGa
@time:  2021/12/03
@des:   sqlite尝试
"""

import sqlite3
import os
from setting import PROJECT_PATH

db_path = os.path.join(PROJECT_PATH, "db", "test.db")  # 没有会在当前路径下创建一个数据库
conn = sqlite3.connect(db_path)
c = conn.cursor()  # 创建数据库连接对象

create_table = """
create table if not exists person_test(
    id int primary key,
    name text not null,
    age int
)
"""

c.execute(create_table)

conn.commit()

# 插入
insert_sql = "insert into person_test(id, name,age) values (1,'cjj', 25)"
try:
    c.execute(insert_sql)
    conn.commit()
except Exception as e:
    print(e)

# 查询
select_sql = "select * from person_test"
t = c.execute(select_sql)
for row in t:
    print(row)

# 更新
update_sql = "update person_test set age = 25 where id = 1"
c.execute(update_sql)
conn.commit()

# 删除
delete_sql = "delete from person_test where id = 1"
c.execute(delete_sql)
conn.commit()
