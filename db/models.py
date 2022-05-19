#!/usr/bin/python
# -*- coding: UTF-8 -*
"""
@author: gaoxiaolong
@time: 2021/10/27
"""

import json

import peewee
from peewee import (
    JOIN,
    SQL,
    CharField,
    DateTimeField,
    IntegerField,
    MySQLDatabase,
    TextField,
)

from utils.constant_utils import JobStatusConstant, JobType, StatType
from utils.core_utils import current_time
from utils.setting import MYSQL_DB, MYSQL_HOST, MYSQL_PASS, MYSQL_PORT, MYSQL_USER

DB = MySQLDatabase(
    MYSQL_DB,
    **{
        'charset': 'utf8',
        'sql_mode': 'PIPES_AS_CONCAT',
        'use_unicode': True,
        'host': MYSQL_HOST,
        'port': MYSQL_PORT,
        'user': MYSQL_USER,
        'password': str(MYSQL_PASS),
    }
)

"""
python -m pwiz -e mysql -H 192.168.1.180 -p 3306 -u fate -P  -t dms_dataset,dms_dataset_version,dms_dataset_version_stat,dms_job fate_flow > db/model.py
需要改成JSONField
connect_info
run_time_config
"""


class JSONField(TextField):
    def db_value(self, value):
        return value if not value else json.dumps(value)

    def python_value(self, value):
        return value if not value else json.loads(value)


class BaseModel(peewee.Model):
    class Meta:
        database = DB

    def to_dict(self):
        data = self.__dict__['__data__']
        for key, value in self.__dict__.items():
            if key not in ('__data__', '_dirty', '__rel__'):
                data[key] = value
        for key in list(data.keys()):
            if key in ['created_at', 'start_at', 'end_at']:
                if data[key]:
                    data[key] = data[key].strftime('%Y-%m-%d %H:%M:%S')
                else:
                    data[key] = ""
            elif key == 'stat_type':
                data[key] = StatType(data[key]).name.lower()
            elif key == 'status':
                data[key] = JobStatusConstant(data[key]).name.lower()
            elif key == 'type':
                data[key] = JobType(data[key]).name.lower()
            elif key in ("updated_at", "is_deleted"):
                data.pop(key)
        return data


class DmsDataset(BaseModel):
    created_at = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    is_deleted = IntegerField(constraints=[SQL("DEFAULT 0")])
    name = CharField(index=True)
    updated_at = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])

    class Meta:
        table_name = 'dms_dataset'

    @classmethod
    def get_by_id(cls, pk):
        with DB.connection_context():
            return cls.get_or_none(cls._meta.primary_key == pk, cls.is_deleted == 0)

    @classmethod
    def get_by_name(cls, name):
        with DB.connection_context():
            return cls.get_or_none(cls.name == name, cls.is_deleted == 0)

    @classmethod
    def create_dataset(cls, name):
        with DB.connection_context():
            return cls.create(name=name)

    @classmethod
    def delete_by_id(cls, pk):
        with DB.connection_context():
            cls.update({"is_deleted": 1}).where(cls._meta.primary_key == pk).execute()

    @classmethod
    def select_all(cls, page_start=1, page_size=10000):
        with DB.connection_context():
            data = (
                cls.select()
                .where(cls.is_deleted == 0)
                .order_by(cls.id)
                .paginate(page_start, page_size)
            )
            return [i.to_dict() for i in data]


class DmsDatasetVersion(BaseModel):
    created_at = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    dataset_id = IntegerField()
    feature_names = TextField(null=True)
    id_name = CharField(constraints=[SQL("DEFAULT ''")])
    is_deleted = IntegerField(constraints=[SQL("DEFAULT 0")])
    stat_type = IntegerField()
    updated_at = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    version = CharField()

    class Meta:
        table_name = 'dms_dataset_version'
        indexes = ((('dataset_id', 'version'), False),)

    @classmethod
    def get_by_id(cls, pk):
        with DB.connection_context():
            return cls.get_or_none(cls._meta.primary_key == pk, cls.is_deleted == 0)

    @classmethod
    def get_by_name(cls, dataset_id, version):
        with DB.connection_context():
            return cls.get_or_none(
                cls.dataset_id == dataset_id,
                cls.version == version,
                cls.is_deleted == 0,
            )

    @classmethod
    def create_version(cls, dataset_id, version, stat_type):
        with DB.connection_context():
            return cls.create(
                dataset_id=dataset_id, version=version, stat_type=stat_type
            )

    @classmethod
    def update_version(cls, version_id, **kwargs):
        with DB.connection_context():
            field = {}
            for key, value in kwargs.items():
                if hasattr(cls, key):
                    field[key] = value
            if field:
                cls.update(field).where(cls._meta.primary_key == version_id).execute()

    @classmethod
    def delete_by_id(cls, pk):
        with DB.connection_context():
            cls.update({"is_deleted": 1}).where(cls._meta.primary_key == pk).execute()

    @classmethod
    def delete_by_dataset_id(cls, dataset_id):
        with DB.connection_context():
            cls.update({"is_deleted": 1}).where(cls.dataset_id == dataset_id).execute()

    @classmethod
    def select_by_dataset_id(cls, dataset_id, page_start=1, page_size=10000):
        with DB.connection_context():
            data = (
                cls.select()
                .where((cls.dataset_id == dataset_id) & (cls.is_deleted == 0))
                .order_by(cls.id)
                .paginate(page_start, page_size)
            )
            return [i.to_dict() for i in data]


class DmsDatasetVersionStat(BaseModel):
    created_at = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    data_count = IntegerField()
    import_type = CharField()
    is_deleted = IntegerField(constraints=[SQL("DEFAULT 0")])
    data_type = IntegerField(constraints=[SQL("DEFAULT 0")])
    stat_time = IntegerField()
    table_name = CharField()
    updated_at = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    version_id = IntegerField()

    class Meta:
        table_name = 'dms_dataset_version_stat'
        indexes = ((('version_id', 'stat_time'), False),)

    @classmethod
    def get_by_id(cls, pk):
        with DB.connection_context():
            return cls.get_or_none(cls._meta.primary_key == pk, cls.is_deleted == 0)

    @classmethod
    def get_by_name(cls, version_id, stat_time):
        with DB.connection_context():
            return cls.get_or_none(
                cls.version_id == version_id,
                cls.stat_time == stat_time,
                cls.is_deleted == 0,
            )

    @classmethod
    def create_stat(
        cls, version_id, stat_time, data_count, import_type, data_type, table_name
    ):
        with DB.connection_context():
            return cls.create(
                version_id=version_id,
                stat_time=stat_time,
                data_count=data_count,
                import_type=import_type,
                data_type=data_type,
                table_name=table_name,
            )

    @classmethod
    def delete_by_dataset_id(cls, dataset_id):
        with DB.connection_context():
            version_objs = DmsDatasetVersion.select().where(
                (DmsDatasetVersion.dataset_id == dataset_id)
                & (DmsDatasetVersion.is_deleted == 0)
            )
            if version_objs:
                for version_obj in version_objs:
                    objs = cls.select().where(
                        (cls.version_id == version_obj.id) & (cls.is_deleted == 0)
                    )
                    if objs:
                        for obj in objs:
                            cls.update({"is_deleted": 1}).where(
                                cls._meta.primary_key == obj.id
                            ).execute()

    @classmethod
    def delete_by_id(cls, pk):
        with DB.connection_context():
            cls.update({"is_deleted": 1}).where(cls._meta.primary_key == pk).execute()

    @classmethod
    def delete_by_version_id(cls, version_id):
        with DB.connection_context():
            cls.update({"is_deleted": 1}).where(cls.version_id == version_id).execute()

    @classmethod
    def select_by_version_id(cls, version_id, page_start=1, page_size=10000):
        with DB.connection_context():
            data = (
                cls.select(
                    cls,
                    DmsDataset.name.alias('dataset'),
                    DmsDatasetVersion.version,
                    DmsDatasetVersion.stat_type,
                    DmsDatasetVersion.id_name,
                    DmsDatasetVersion.feature_names,
                    DmsDatasetVersion.dataset_id,
                )
                .join(
                    DmsDatasetVersion,
                    JOIN.INNER,
                    on=(cls.version_id == DmsDatasetVersion.id),
                )
                .join(
                    DmsDataset,
                    JOIN.INNER,
                    on=(DmsDatasetVersion.dataset_id == DmsDataset.id),
                )
                .where(
                    (cls.version_id == version_id)
                    & (cls.is_deleted == 0)
                    & (DmsDataset.is_deleted == 0)
                    & (DmsDatasetVersion.is_deleted == 0)
                )
                .order_by(cls.id)
                .paginate(page_start, page_size)
            )
            return [i.to_dict() for i in data.objects()]

    @classmethod
    def get_info_by_id(cls, stat_id):
        with DB.connection_context():
            data = (
                cls.select(
                    cls,
                    DmsDataset.name.alias('dataset'),
                    DmsDatasetVersion.version,
                    DmsDatasetVersion.stat_type,
                    DmsDatasetVersion.id_name,
                    DmsDatasetVersion.feature_names,
                    DmsDatasetVersion.dataset_id,
                )
                .join(
                    DmsDatasetVersion,
                    JOIN.INNER,
                    on=(cls.version_id == DmsDatasetVersion.id),
                )
                .join(
                    DmsDataset,
                    JOIN.INNER,
                    on=(DmsDatasetVersion.dataset_id == DmsDataset.id),
                )
                .where(
                    (cls.id == stat_id)
                    & (cls.is_deleted == 0)
                    & (DmsDataset.is_deleted == 0)
                    & (DmsDatasetVersion.is_deleted == 0)
                )
            )
            result = [i.to_dict() for i in data.objects()]
            return result[0] if len(result) > 0 else {}


class DmsJob(BaseModel):
    celery_id = CharField(null=True)
    created_at = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    data_count = IntegerField(null=True)
    end_at = DateTimeField(null=True)
    is_deleted = IntegerField(constraints=[SQL("DEFAULT 0")])
    job_code = CharField(index=True)
    proceed_data_count = IntegerField(constraints=[SQL("DEFAULT 0")])
    result = JSONField(null=True)  # json
    run_time_config = JSONField(null=True)  # json
    start_at = DateTimeField(null=True)
    status = IntegerField()
    type = IntegerField()
    updated_at = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])

    class Meta:
        table_name = 'dms_job'

    @classmethod
    def get_by_job_id(cls, job_id):
        with DB.connection_context():
            return cls.get_or_none(cls.job_code == job_id, cls.is_deleted == 0)

    @classmethod
    def failed_job(cls, job_id):
        with DB.connection_context():
            cls.update(
                {"status": JobStatusConstant.FAILED.value, "end_at": current_time()}
            ).where(cls.job_code == job_id).execute()

    @classmethod
    def succeed_job(cls, job_id):
        with DB.connection_context():
            cls.update(
                {"status": JobStatusConstant.SUCCEED.value, "end_at": current_time()}
            ).where(cls.job_code == job_id).execute()

    @classmethod
    def canceled_job(cls, job_id):
        with DB.connection_context():
            cls.update({"status": JobStatusConstant.CANCELED.value}).where(
                cls.job_code == job_id
            ).execute()

    @classmethod
    def running_job(cls, job_id):
        with DB.connection_context():
            cls.update(
                {"status": JobStatusConstant.RUNNING.value, "start_at": current_time()}
            ).where(cls.job_code == job_id).execute()

    @classmethod
    def create_job(cls, job_id, import_type, run_time_config):
        with DB.connection_context():
            return cls.create(
                job_code=job_id,
                type=import_type,
                run_time_config=run_time_config,
                status=JobStatusConstant.WAITING.value,
            )

    @classmethod
    def update_job(cls, job_id, **kwargs):
        with DB.connection_context():
            field = {}
            for key, value in kwargs.items():
                if hasattr(cls, key):
                    field[key] = value
            if field:
                cls.update(field).where(cls.job_code == job_id).execute()

    @classmethod
    def select_ready_job(cls):
        with DB.connection_context():
            return cls.select().where(
                cls.status == JobStatusConstant.WAITING.value,
                (
                    (cls.type == JobType.API_OFFLINE.value)
                    | (cls.type == JobType.DOWNLOAD_BY_SELF.value)
                ),
            )


def init_tables():
    DB.create_tables([DmsJob, DmsDatasetVersionStat, DmsDataset, DmsDatasetVersion])
