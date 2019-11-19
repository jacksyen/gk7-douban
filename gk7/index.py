#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import web
import json

import globals as gl
from send import Send
from util.log import logger
from db.dbase import Database

# 设置系统编码
# reload(sys)
# sys.setdefaultencoding('utf-8')


urls = (
    '/','Index',
    '/send', 'Send'
)

if gl.ENV == 'ONLINE':
    web.config.debug = False
app = web.application(urls, globals())

class Index:

    def GET(self):
        return json.dumps({'msg':'not services'})

    def POST(self):
        return json.dumps({'msg':'not servicindex'})

if __name__ == "__main__":
    logger.info(u'-----------系统启动-----------')
    Database()
    #web.wsgi.runwsgi = lambda func, addr=None: web.wsgi.runfcgi(func, addr)   ##这行是新增的
    app.run()

if gl.ENV == 'ONLINE':
    application = app.wsgifunc()
