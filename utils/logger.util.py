#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:  BryanGa
@time:  2021/11/17
@des:   日志模块
"""

# https://pypi.org/project/loguru/
import sys
from functools import lru_cache

from loguru import logger
from setting import LOG_LEVEL

_format = (
    '<g>{time:YYYY-MM-DD HH:mm:ss}</g> '
    '| <level>{level: <8}</level> '
    '| <e>{thread.name: <10}</e> '
    '| <fg #CF55E8>{extra[utc]: <18}</fg #CF55E8>'
    '| <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> '
    '- <level>{message}</level>'
)

logger.remove(0)  # 移除默认的handler
# logger.add(sys.stderr, format=_format, level=LOG_LEVEL)
logger.add(sys.stderr, format="{time} {level} {message}", level=LOG_LEVEL)
logger.add("file_log.log")  # 指定文件路径

# @lru_cache()
# def practice_logger():
#     pass


if __name__ == "__main__":
    logger.info("This is test")
