# -*- coding:utf-8 -*-
import os
import time, datetime
import logging
import logging.handlers

import webglobal.globals as gk7

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
    def log(error_name=''):
        if not os.path.exists(gk7.LOG_DIRS):
            os.mkdir(gk7.LOG_DIRS)
        # 日志系统
        #filePath = "%s/%s.log" %(gk7.LOG_DIRS, time.strftime("%Y-%m-%d",time.localtime()))
        filePath = '%s/%s%s.log' %(gk7.LOG_DIRS, os.path.abspath('.').split('/')[-1], error_name)
        logging.basicConfig(level=logging.INFO)
        filehandler = logging.handlers.TimedRotatingFileHandler(filePath, when='midnight')
        #filehandler = logging.handlers.TimedRotatingFileHandler(filePath, when='S', interval=1, backupCount=0)
        filehandler.suffix = '%Y-%m-%d'

        formatter = custom_format('%(asctime)s %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S.%03d')
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
        logg,hdr = logger.log('.error')
        logg.error(msg, *args, **kwargs)
        import traceback
        logg.error(traceback.format_exc())
        hdr.flush()
        logg.removeHandler(hdr)

    @staticmethod
    def unknown(msg, *args, **kwargs):
        logg,hdr = logger.log('.unknown')
        logg.warn(msg, *args, **kwargs)
        hdr.flush()
        logg.removeHandler(hdr)
        
