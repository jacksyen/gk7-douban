# -*- coding:utf-8 -*-
import os
import time
import logging
import logging.handlers

from webglobal.globals import global_logs

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
        filehandler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s', '%Y-%m-%d %H:%M:%S'))
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
