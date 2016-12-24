#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import io
import math
import sys
import time
import traceback
import uuid

# 向下取小数点后decimal_places位精度
def downRound(qty, decimal_places=4):
    return int(qty * math.pow(10, decimal_places)) / int(math.pow(10, decimal_places))


# 对币数量进行精度裁剪
def getRoundedQuantity(qty, coin_type):
    return downRound(qty, decimal_places=2)



# 从对象拿数据
def componentExtract(object, key, default=None):
    if type(object) == dict:
        return object.get(key, default)
    else:
        return getattr(object, key, default)


# 获取uuid
def getUUID():
    return str(uuid.uuid1())


# print traceback to log
def printTracebackToLog(timeLog):
    try:
        output = io.StringIO()
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_tb(exc_traceback, file=output)
        timeLog(output.getvalue())
    finally:
        output.close()


# 获取当前时间，返回字符串，格式为：'YYYYMMDD_hhmmss'
def current_time_str():
    current_time = datetime.datetime.now()
    time_string = current_time.strftime('%Y%m%d_%H%M%S')
    return time_string


# 将时间戳转化为可读时间
def timestamp_to_timestr(timestamp):
    time_struct = time.localtime(timestamp)
    time_string = time.strftime("%Y%m%d_%H%M%S", time_struct)
    return time_string
