#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:  BryanGa
@time:  2022/01/10
@des:   友盟数据上传
"""

from umeng_setting import APIKEY, APISECURITY, APPID

apiKey = APIKEY
apiSecurity = APISECURITY
appId = APPID

"""
apiKey、
apiSecurity name
taskType
appId idType
remarks cuVersions
是 否 必
类型 须 String 是
String 是 Integer 是
Long 是 Integer 是
String 否 umeng.finplus.cuversion[] 否
"""

name = ""
taskType = ""
idType = ""
# 非必需参数
remarks = ""
