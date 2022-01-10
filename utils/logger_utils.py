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
from setting import LOG_LEVEL, LOG_PATH

_format = (
    '<g>{time:YYYY-MM-DD HH:mm:ss}</g> '
    '| <level>{level: <8}</level> '
    '| <e>{thread.name: <10}</e> '
    '| <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> '
    '- <level>{message}</level>'
)

logger.remove(0)  # 移除默认的handler
logger.add(sys.stderr, format=_format, level=LOG_LEVEL)
logger.add(LOG_PATH, rotation="500 MB")  # 指定文件路径和文件大小上限


@lru_cache(500)
@logger.catch()
def test():
    # 保留500个此函数的计算结果
    # 自动捕获异常到日志
    return 1 / 1


if __name__ == "__main__":
    logger.info("This is test")
    test()
