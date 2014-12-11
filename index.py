#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import web
import json
import base64
import threading

from helper.log import logger
from helper.init import Init_DB
from helper.mail import SendMail
from helper.page import HTML

from trans.send import Send


# 设置系统编码
reload(sys)
sys.setdefaultencoding('utf-8')


urls = (
    '/','Index',
    '/send', 'Send',
)
#web.config.debug = False
app = web.application(urls, globals())

class Index:

    def GET(self):
        return json.dumps({'msg':'not services'})

    def POST(self):
        return json.dumps({'msg':'not servicindex'})

if __name__ == "__main__":
    logger.info(u'-----------系统启动-----------')
    # 初始化数据库和表信息
    Init_DB.init()

    #web.wsgi.runwsgi = lambda func, addr=None: web.wsgi.runfcgi(func, addr)   ##这行是新增的
    app.run()
