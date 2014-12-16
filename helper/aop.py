#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
author by jacksyen[hyqiu.syen@gmail.com]
---------------------------------------
切面帮助类
"""
import time
from log import logger

def exec_time(func):
    def wrapper(*args, **args2):
        time.clock()
        logger.info(u"调用函数:{%s.%s}，入参：%s" %(func.__module__, func.__name__, str(args)))
        back = func(*args, **args2)
        logger.info("调用函数:{%s.%s}，出参：%s，耗时：%.3fs" %(func.__module__, func.__name__, str(back), time.clock()))
        return back
    return wrapper
