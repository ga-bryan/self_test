CREATE DATABASE IF NOT EXISTS dms DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;

USE dms;

CREATE TABLE IF NOT EXISTS dms_dataset
(
    `id`         int         NOT NULL AUTO_INCREMENT COMMENT '编号' primary key,
    `name`       varchar(64) NOT NULL COMMENT '数据集名称',
    `is_deleted` tinyint     NOT NULL DEFAULT 0 COMMENT '是否删除 0：不删除，1：删除',
    `created_at` datetime    NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at` datetime    NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '创建时间',
    INDEX (name)
);

CREATE TABLE IF NOT EXISTS dms_dataset_version
(
    `id`            int         NOT NULL AUTO_INCREMENT COMMENT '编号' primary key,
    `dataset_id`    int         NOT NULL COMMENT '数据集编号',
    `version`       varchar(64) NOT NULL COMMENT '数据集版本',
    `stat_type`     tinyint     NOT NULL COMMENT '回溯类型：0:按日回溯;1:按月回溯',
    `id_name`       varchar(64) NOT NULL DEFAULT '' COMMENT '数仓表id名称',
    `feature_names` text        NULL COMMENT '数仓特征列名',
    `is_deleted`    tinyint     NOT NULL DEFAULT 0 COMMENT '是否删除 0：不删除，1：删除',
    `created_at`    datetime    NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at`    datetime    NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX (dataset_id, version)
);

CREATE TABLE IF NOT EXISTS dms_dataset_version_stat
(
    `id`          int         NOT NULL AUTO_INCREMENT COMMENT '编号' primary key,
    `version_id`  int         NOT NULL COMMENT '数据集版本编号',
    `stat_time`   int         NOT NULL COMMENT '回溯时间',
    `table_name`  varchar(64) NOT NULL COMMENT '数仓表名',
    `import_type` varchar(32) NOT NULL COMMENT '导入类型 LOCAL,FTP,HTTP,HIVE,CLICKHOUSE',
    `data_type`   tinyint     NOT NULL COMMENT '数据类型 0：数据源,1：SDN应用方,2：DPPC应用方',
    `data_count`  int         NOT NULL COMMENT '数据总数',
    `is_deleted`  tinyint     NOT NULL DEFAULT 0 COMMENT '是否删除 0：不删除，1：删除',
    `created_at`  datetime    NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at`  datetime    NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX (version_id, stat_time)
);


CREATE TABLE IF NOT EXISTS dms_job
(
    `id`                 int         NOT NULL AUTO_INCREMENT COMMENT '编号' primary key,
    `job_code`           varchar(64) NOT NULL UNIQUE COMMENT '任务code ',
    `celery_id`          varchar(64) NULL COMMENT '异步任务id',
    `type`               tinyint     NOT NULL COMMENT ' 任务类型, 0: IMPORT, 1:EXPORT_ID，2:EXPORT_FEATURE',
    `run_time_config`    json        NULL COMMENT '任务配置',
    `start_at`           datetime    NULL COMMENT '起始时间',
    `end_at`             datetime    NULL COMMENT '结束时间',
    `status`             tinyint     NOT NULL COMMENT ' 状态，WAITING:0,RUNNING:1,FAILED:2,SUCCEED:3,CANCELED:4',
    `data_count`         int         NULL COMMENT ' 数据总数 ',
    `proceed_data_count` int         NOT NULL DEFAULT 0 COMMENT ' 已完成数据计数 ',
    `result`             json        NULL COMMENT '任务结果',
    `is_deleted`         tinyint     NOT NULL DEFAULT 0 COMMENT '是否删除 0：不删除，1：删除',
    `created_at`         datetime    NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at`         datetime    NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX (job_code)
);


