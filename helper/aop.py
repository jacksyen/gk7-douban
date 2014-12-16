#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
author by jacksyen[hyqiu.syen@gmail.com]
---------------------------------------
切面帮助类
"""
import time
from log import logger

'''
打印调用函数信息，包括参数，运行时间
'''
def exec_time(func):
    def wrapper(*args, **args2):
        t0 = time.time()
        logger.info(u"调用函数:{%s.%s}，入参：%s" %(func.__module__, func.__name__, str(args)))
        back = func(*args, **args2)
        if not back:
            back = ''
        logger.info("调用函数:{%s.%s}，出参：%s，耗时：%.3fs" %(func.__module__, func.__name__, str(back), time.time() - t0))
        return back
    return wrapper

'''
打印调用函数输入信息，包括调用信息
输出信息，包括参数，运行时间
'''
def exec_out_time(func):
    def wrapper(*args, **args2):
        t0 = time.time()
        logger.info(u"调用函数:{%s.%s}" %(func.__module__, func.__name__))
        back = func(*args, **args2)
        logger.info("调用函数:{%s.%s}，出参：%s，耗时：%.3fs" %(func.__module__, func.__name__, str(back), time.time() - t0))
        return back
    return wrapper

'''
打印调用函数耗时信息
'''
def exec_time_consum(func):
    def wrapper(*args, **args2):
        t0 = time.time()
        logger.info(u"调用函数:{%s.%s}" %(func.__module__, func.__name__))
        back = func(*args, **args2)
        logger.info("调用函数:{%s.%s}，耗时：%.3fs" %(func.__module__, func.__name__, time.time() - t0))
        return back
    return wrapper
