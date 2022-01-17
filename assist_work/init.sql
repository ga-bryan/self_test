
CREATE SCHEMA IF NOT EXISTS `sdn` DEFAULT CHARACTER SET utf8;

use sdn;

CREATE TABLE IF NOT EXISTS `host_data`
(
    `id`              BIGINT           NOT NULL AUTO_INCREMENT COMMENT '主键id',
    `data_code`       VARCHAR(45)      NOT NULL COMMENT '数据code',
    `name`            VARCHAR(45)      NOT NULL COMMENT '数据名称',
    `description`     VARCHAR(110)     NULL COMMENT '数据概述',
    `status`          TINYINT UNSIGNED NOT NULL DEFAULT 0 COMMENT '数据集状(0: 未发布 1: 已发布 2: 已下架)',
    `id_encrypt_type` TINYINT UNSIGNED NOT NULL DEFAULT 0 COMMENT '加密方式(0: MD5 1: SHA256 2: SM3 3: RAW)',
    `created_at`      DATETIME         NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at`      DATETIME         NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
    `is_deleted`      TINYINT          NOT NULL DEFAULT 0 COMMENT '逻辑删除(0: 未删除 1: 已删除)',
    PRIMARY KEY (`id`),
    UNIQUE INDEX `data_id_UNIQUE` (`data_code` ASC) VISIBLE
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
    COMMENT = '数据源方-数据表';

CREATE TABLE IF NOT EXISTS `host_data_version`
(
    `id`             BIGINT       NOT NULL COMMENT '主键id',
    `data_id`        BIGINT       NOT NULL COMMENT '数据id',
    `version`        VARCHAR(45)  NOT NULL COMMENT '版本号',
    `import_type`    TINYINT      NOT NULL DEFAULT 0 COMMENT '数据导入方式(0: CSV 1: 数据库 2: 定时任务)',
    `stat_type`      TINYINT      NOT NULL DEFAULT 0 COMMENT '回溯方式(0: 按月 1: 按日)',
    `stat_begin`     DATE         NULL COMMENT '最早可回溯时间',
    `stat_end`       DATE         NULL COMMENT '最晚可回溯时间',
    `id_map`         JSON         NULL COMMENT '匹配键映射字段',
    `tag_map`        JSON         NULL COMMENT '特征分组',
    `dimension`      INT          NULL COMMENT '特征维度',
    `count`          INT          NULL COMMENT '数据量',
    `status`         TINYINT      NOT NULL DEFAULT 0 COMMENT '状态(0: 待审核 1: 未通过 2: 数据上传中 3: 已发布 4: 发布失败 5: 已下架)',
    `dms_stat_id`    BIGINT       NULL COMMENT 'DMS数据版本id',
    `publisher_id`   BIGINT       NULL COMMENT '发布人员id',
    `auditor_id`     BIGINT       NULL COMMENT '审批人员id',
    `created_at`     DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at`     DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
    `online_db_url`  VARCHAR(110) NULL COMMENT '在线数据库接口地址',
    `offline_db_url` VARCHAR(110) NULL COMMENT '离线数据库接口地址',
    `is_deleted`     TINYINT      NOT NULL DEFAULT 0 COMMENT '逻辑删除(0: 未删除 1: 已删除)',
    PRIMARY KEY (`id`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
    COMMENT = '数据源方-数据版本信息表';

CREATE TABLE IF NOT EXISTS `host_data_upload`
(
    `id`              BIGINT       NOT NULL AUTO_INCREMENT COMMENT '主键id',
    `version_id`      BIGINT       NULL COMMENT '数据版本id',
    `fate_namespace`  VARCHAR(50)  NULL COMMENT 'fate表空间',
    `fate_table_name` VARCHAR(50)  NULL COMMENT 'fate表名',
    `time_spec`       DATE         NULL COMMENT '回溯时间点',
    `status`          TINYINT      NOT NULL DEFAULT 0 COMMENT '状态(0: 上传中 1: 已完成 2: 已失败)',
    `fail_reason`     VARCHAR(255) NULL COMMENT '失败原因',
    `creator_id`      BIGINT       NULL COMMENT '创建者id',
    `created_at`      DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at`      DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
    `is_deleted`      TINYINT      NOT NULL DEFAULT 0 COMMENT '逻辑删除(0: 未删除 1:已删除)',
    PRIMARY KEY (`id`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
    COMMENT = '数据源方-数据上传信息表';

CREATE TABLE IF NOT EXISTS `host_data_approve`
(
    `id`             BIGINT   NOT NULL AUTO_INCREMENT COMMENT '主键id',
    `data_id`        BIGINT   NOT NULL COMMENT '数据集id',
    `apply_party_id` BIGINT   NOT NULL COMMENT '申请方id',
    `price_rule_id`  BIGINT   NOT NULL COMMENT '计价策略id',
    `approver_id`    BIGINT   NULL COMMENT '审批人员id',
    `status`         TINYINT  NOT NULL DEFAULT 0 COMMENT '状态(0: 待审批 1: 已合作 2: 已拒绝)',
    `created_at`     DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '申请日期',
    `approved_at`    DATETIME NULL COMMENT '审批时间',
    `updated_at`     DATETIME NULL     DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
    `is_deleted`     TINYINT  NOT NULL DEFAULT 0 COMMENT '逻辑删除(0: 未删除 1:已删除)',
    PRIMARY KEY (`id`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
    COMMENT = '数据源方-数据审批表';

CREATE TABLE IF NOT EXISTS `host_services_approve`
(
    `id`           BIGINT      NOT NULL AUTO_INCREMENT COMMENT '主键id',
    `predict_code` VARCHAR(45) NULL COMMENT '预测code',
    `model_code`   VARCHAR(45) NULL COMMENT '模型code',
    `data_id`      BIGINT      NULL COMMENT '数据id',
    `type`         TINYINT     NOT NULL DEFAULT 0 COMMENT '预测类型(0 在线 1 离线)',
    `is_cron`      TINYINT     NOT NULL DEFAULT 0 COMMENT '是否定时任务(0 单次 1 定时, 仅type为1时有效)',
    `status`       TINYINT     NOT NULL DEFAULT 0 COMMENT '状态(0 待审批 1 已发布 2 已拒绝 3 发布失败)',
    `approver_id`  BIGINT      NULL COMMENT '审批人员id',
    `created_at`   DATETIME    NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `approved_at`  DATETIME    NULL COMMENT '审批时间',
    `is_deleted`   TINYINT     NOT NULL DEFAULT 0 COMMENT '逻辑删除(0 未删除 1 已删除)',
    PRIMARY KEY (`id`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
    COMMENT = '数据源方-服务审批表';

CREATE TABLE IF NOT EXISTS `host_upload_timer`
(
    `id`         BIGINT      NOT NULL AUTO_INCREMENT COMMENT '主键id',
    `version_id` BIGINT      NOT NULL COMMENT '数据版本id',
    `frequency`  INT         NULL COMMENT '导入频率(日时分或时分格式, 如200830表示每个月20号8点半)',
    `db_type`    TINYINT     NOT NULL DEFAULT 0 COMMENT '数据库类型(0: hive 1: mysql 2: oracle)',
    `db_addr`    VARCHAR(45) NULL COMMENT '数据库地址和端口',
    `db_name`    VARCHAR(45) NULL COMMENT '数据库名',
    `table_name` VARCHAR(45) NULL COMMENT '数据表名',
    `username`   VARCHAR(45) COMMENT '用户名',
    `password`   VARCHAR(45) NULL COMMENT '密码',
    PRIMARY KEY (`id`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
    COMMENT = '数据源方-数据上传定时任务信息表';

CREATE TABLE IF NOT EXISTS `host_data_friend`
(
    `id`         BIGINT NOT NULL AUTO_INCREMENT COMMENT '主键id',
    `data_id`    BIGINT NOT NULL COMMENT '数据集id',
    `company_id` BIGINT NOT NULL COMMENT '商户id',
    PRIMARY KEY (`id`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
    COMMENT = '数据源方-数据可见商户表';

CREATE TABLE IF NOT EXISTS `host_partner_site`
(
    `id`                   bigint       NOT NULL AUTO_INCREMENT COMMENT 'PK',
    `partner_name`         varchar(64)  NOT NULL COMMENT '公司名称',
    `site_name`            varchar(64)           DEFAULT NULL COMMENT '站点名称',
    `site_ip_addr`         varchar(64)           DEFAULT NULL COMMENT '站点地址',
    `party_id`             varchar(16)  NOT NULL COMMENT '合作方站点id',
    `fate_version`         varchar(16)           DEFAULT NULL COMMENT 'FATE版本',
    `fate_serving_version` varchar(16)           DEFAULT NULL COMMENT 'FATE-Serving版本',
    `status`               tinyint(2)            DEFAULT NULL COMMENT '状态,0:使用中,1:已停用',
    `created_at`           datetime NOT NULL DEFAULT CURRENT_TIMESTAMP() COMMENT '创建时间',
    `updated_at`           datetime NOT NULL DEFAULT CURRENT_TIMESTAMP() ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间',
    PRIMARY KEY (`id`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_0900_ai_ci
    COMMENT = '数据源-合作方资源信息表';

CREATE TABLE IF NOT EXISTS `host_online_service`
(
    `id`         bigint       NOT NULL AUTO_INCREMENT COMMENT 'PK',
    `code`       bigint                DEFAULT NULL COMMENT '在线预测服务ID',
    `model_code` varchar(128)          DEFAULT NULL COMMENT '模型ID',
    `data_id`    bigint                DEFAULT NULL COMMENT '数据集主键',
    `data_code`  varchar(128)          DEFAULT NULL COMMENT '数据集ID',
    `auditor_id` bigint                DEFAULT NULL COMMENT '审批人主键',
    `auditor`    varchar(64)           DEFAULT NULL COMMENT '审批人',
    `status`     tinyint(3)            DEFAULT NULL COMMENT '状态,0:未通过,1:审核中,2:已发布',
    `offered_at` DATETIME     NOT NULL COMMENT '提交日期',
    `audited_at` DATETIME     NOT NULL COMMENT '审批日期',
    `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间',
    PRIMARY KEY (`id`)
) ENGINE = InnoDB
  AUTO_INCREMENT = 1
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_0900_ai_ci
    COMMENT ='数据源-在线预测服务表';


DROP TABLE IF EXISTS host_bill;
CREATE TABLE `host_bill`
(
    `id`              bigint       NOT NULL AUTO_INCREMENT COMMENT 'PK',
    `date`            date                  DEFAULT NULL COMMENT '日期',
    `partner_id`      bigint       NOT NULL COMMENT '应用方id',
    `partner_name`    varchar(64)           DEFAULT NULL COMMENT '应用方名称',
    `data_id`         bigint       NOT NULL COMMENT '数据集pk',
    `data_code`       varchar(25)           DEFAULT NULL COMMENT '数据集ID',
    `data_version_id` bigint                DEFAULT NULL COMMENT '数据版本pk',
    `data_version`    varchar(20)           DEFAULT NULL COMMENT '数据版本名称',
    `call_type`       tinyint(2)            DEFAULT NULL COMMENT '调用类型(0:在线+离线;1:在线预测;2:离线预测)',
    `call_count`      int                   DEFAULT NULL COMMENT '调用次数(成功次数)',
    `hit_count`       int                   DEFAULT NULL COMMENT '成功次数(查得次数)',
    `error_count`     int                   DEFAULT NULL COMMENT '错误次数',
    `cost_type`       tinyint(5)            DEFAULT NULL COMMENT '计费方式(1:查得,2:查询,3:打包,4:阶梯)',
    `auto_cost`       float                 DEFAULT NULL COMMENT '系统计算费用',
    `edit_cost`       float                 DEFAULT NULL COMMENT '手动调整费用',
    `created_at`      timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at`      timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间',
    PRIMARY KEY (`id`)
) ENGINE = InnoDB
  AUTO_INCREMENT = 1
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_0900_ai_ci COMMENT ='数据源-账单统计表';

DROP TABLE IF EXISTS `host_bill_strategy`;
CREATE TABLE `host_bill_strategy`
(
    `id`                bigint       NOT NULL AUTO_INCREMENT COMMENT 'PK',
    `name`              varchar(128)          DEFAULT NULL COMMENT '产品名称',
    `data_id`           bigint       NOT NULL COMMENT '数据集pk',
    `data_code`         varchar(25)           DEFAULT NULL COMMENT '数据集ID',
    `call_type`         tinyint(2)            DEFAULT NULL COMMENT '调用类型(0:在线+离线;1:在线预测;2:离线预测)',
    `strategy_type`     tinyint(2)            DEFAULT NULL COMMENT '计费类型(0:全部商户,1:部分商户)',
    `partner_id`        bigint                DEFAULT NULL COMMENT '应用方id',
    `partner_name`      varchar(64)           DEFAULT NULL COMMENT '应用方名称',
    `cost_type`         tinyint(5)            DEFAULT NULL COMMENT '计费方式(1:查得,2:查询,3:打包,4:阶梯)',
    `package_cost_type` tinyint(2)            DEFAULT NULL COMMENT '打包下计费口径(1:查得,2:查询)',
    `single_price`      double                DEFAULT NULL COMMENT '单价(元/次)-仅限查得、查询、打包',
    `package_price`     double                DEFAULT NULL COMMENT '打包总额(元)-仅限打包',
    `package_count`     int                   DEFAULT NULL COMMENT '折合次数-仅限打包',
    `over_price`        double                DEFAULT NULL COMMENT '超出单价(元/次)-仅限打包',
    `stepwise_price`    json                  DEFAULT NULL COMMENT '阶梯计价',
    `remark`            varchar(128)          DEFAULT NULL COMMENT '备注',
    `created_at`        timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at`        timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间',
    PRIMARY KEY (`id`)
) ENGINE = InnoDB
  AUTO_INCREMENT = 1
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_0900_ai_ci COMMENT ='数据源-计费策略';