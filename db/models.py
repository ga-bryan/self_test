#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:  BryanGa
@time:  2021/11/11
@des:   
"""

import json

import peewee
from peewee import (SQL, BigAutoField, CharField, DateTimeField, IntegerField,
                    Model, TextField)

from peewee import MySQLDatabase

from setting import MYSQL_HOST, MYSQL_PORT, MYSQL_USER
from utils.db_connect import MYSQL_DB


def MYSQL_PASS(args):
    pass


DB = MySQLDatabase(
    MYSQL_DB,
    **{
        'charset': 'utf8',
        'sql_mode': 'PIPES_AS_CONCAT',
        'use_unicode': True,
        'host': MYSQL_HOST,
        'port': MYSQL_PORT,
        'user': MYSQL_USER,
        'password': MYSQL_PASS,
    }
)


class BaseModel(Model):
    class Meta:
        database = DB


class JobFindModel:
    @staticmethod
    def find_by_code(self_code, aim_code):
        if self_code == aim_code: return True
        return False


class JSONField(peewee.TextField):
    def db_value(self, value):
        """Convert the python value for storage in the database."""
        return value if value is None else json.dumps(value)

    def python_value(self, value):
        """Convert the database value to a pythonic value."""
        return value if value is None else json.loads(value)


class Job(BaseModel, JobFindModel):
    code = CharField()
    completed_at = DateTimeField(null=True)
    created_at = DateTimeField(
        constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")], null=True
    )
    description = CharField(null=True)
    id = BigAutoField()
    is_deleted = IntegerField(constraints=[SQL("DEFAULT 0")])
    name = CharField(null=True)
    project_code = CharField()
    status = IntegerField(constraints=[SQL("DEFAULT 0")])
    type = IntegerField()
    updated_at = DateTimeField(
        constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")], null=True
    )
    updated_id = IntegerField(null=True)
    user_id = IntegerField(null=True)

    class Meta:
        table_name = 'cs_job'
        indexes = ((('project_code', 'code'), True),)


class JobData(BaseModel):
    code = CharField(index=True)
    data_code = CharField()
    id = BigAutoField()

    class Meta:
        table_name = 'cs_job_data'


class JobInfoModel(BaseModel):
    alg_type = IntegerField(null=True)
    code = CharField(unique=True)
    config = JSONField(null=True)  # json
    id = BigAutoField()
    log = TextField(null=True)
    model_name = CharField(null=True)

    class Meta:
        table_name = 'cs_job_info_model'


class JobInfoPredict(BaseModel):
    code = CharField(unique=True)
    id = BigAutoField()
    log = TextField(null=True)
    model_code = CharField(null=True)
    model_name = CharField(null=True)

    class Meta:
        table_name = 'cs_job_info_predict'


class JobInfoQuery(BaseModel):
    code = CharField(unique=True)
    id = BigAutoField()
    log = TextField(null=True)
    result = TextField(null=True)
    statement = CharField()
    supported_func = CharField(null=True)

    class Meta:
        table_name = 'cs_job_info_query'


if __name__ == "__main__":
    create_data = True
    create_data = False
    create_data_base = True
    create_data_base = False

    if create_data:
        job = Job(code="108", description="today's test")
        job.save()
    if create_data_base:
        for t in ["Job", "JobData", "JobInfoModel", "JobInfoQuery"]:
            eval(t).create_table()
    # job = Job.get(Job.code == "109")
    job = Job.select().where(Job.code == "108")
    if job:
        job = job.get()
        if Job.find_by_code(self_code=job.code, aim_code="108"):
            print("this is data which i wonder")
