# -*- coding:utf-8 -*-
import os
import time, datetime
import logging
import logging.handlers

from webglobal.globals import global_logs

'''
自定义日志时间格式
'''
class custom_format(logging.Formatter):

    converter=datetime.datetime.fromtimestamp
    def formatTime(self, record, datefmt=None):
        ct = self.converter(record.created)
        if datefmt:
            s = ct.strftime(datefmt)
        else:
            t = ct.strftime("%Y-%m-%d %H:%M:%S")
            s = "%s,%03d" % (t, record.msecs)
        return s
'''
日志记录
'''
class logger:

    def __init__(self):
        pass

    @staticmethod
    def log():
        if not os.path.exists(global_logs.LOG_DIRS):
            os.mkdir(global_logs.LOG_DIRS)
        # 日志系统
        #filePath = "%s/%s.log" %(global_logs.LOG_DIRS, time.strftime("%Y-%m-%d",time.localtime()))
        filePath = '%s/%s' %(global_logs.LOG_DIRS, os.path.abspath('.').split('/')[-1])
        logging.basicConfig(level=logging.INFO)
        filehandler = logging.handlers.TimedRotatingFileHandler(filePath, when='d', interval=1, backupCount=0)
        filehandler.suffix = '-%Y-%m-%d.log'

        formatter = custom_format('%(asctime)s %(levelname)s: %(message)s', datefmt='%Y-%m-%d,%H:%M:%S.%f')
        filehandler.setFormatter(formatter)
        logg = logging.getLogger('')
        logg.addHandler(filehandler)
        return logg,filehandler

    @staticmethod
    def info(msg, *args, **kwargs):
        logg,hdr = logger.log()
        logg.info(msg, *args, **kwargs)
        hdr.flush()
        logg.removeHandler(hdr)

    @staticmethod
    def error(msg, *args, **kwargs):
        logg,hdr = logger.log()
        logg.error(msg, *args, **kwargs)
        hdr.flush()
        logg.removeHandler(hdr)
