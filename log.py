# -*- coding:utf-8 -*-
import os
import logging
import logging.handlers


'''
日志记录
'''
class logger:

    def __init__(self):
        pass

    @staticmethod
    def init():
        path = "log"
        if not os.path.exists(path):
            os.mkdir(path)
        # 日志系统
        #filePath = "%s/%s.log" %(path, time.strftime("%Y-%m-%d",time.localtime()))
        filePath = '%s/easylife' %path

        logging.basicConfig(level=logging.INFO)
        filehandler = logging.handlers.TimedRotatingFileHandler(filePath, when='midnight', interval=1, backupCount=0)
        filehandler.suffix = '%Y-%m-%d.log'
        filehandler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s', '%Y-%m-%d %H:%M:%S'))
        logg = None
        logg = logging.getLogger('')
        logg.addHandler(filehandler)
        return [logg,filehandler]

    @staticmethod
    def info(msg):
        logg,hdlr = logger.init()
        logg.log(logging.INFO, msg)
        hdlr.flush()
        logg.removeHandler(hdlr)

    @staticmethod
    def error(msg):
        logg,hdlr = logger.init()
        logg.log(logging.ERROR, msg)
        hdlr.flush()
        logg.removeHandler(hdlr)
