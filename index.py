#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
import web
import json
import base64
import threading

import CloudConvert

from log import logger
from webglobal import Global
from dbase import SQLite
from mail import SendMail
from page import HTML

urls = (
    '/','index',
    '/send', 'send',
)
app = web.application(urls, globals())


class index:

    def GET(self):
        return json.dumps({'msg':'not services'})

    def POST(self):
        return json.dumps({'msg':'not servicindex'})

class send:

    def __init__(self):
        self.conn = SQLite.conn()
        self.db = self.conn.cursor()

    def __del__(self):
        if self.conn:
            SQLite.close(self.conn)
            
    def GET(self):
        return self.execute()

    def POST(self):
        return self.execute()

    def convert(self, filename, convert_filename):
        apikey = 'wGE3hDxkDFdgIJkrnQ9UsdqFFGLdwNpZfVVqjkOjbP5esS6U7JJQQAgg4mgCdgHPzgd8F5W0VoA5WkLlD1e3CA'
        process = CloudConvert.ConversionProcess(apikey)
        process.init(filename, convert_filename)
        process.start()
        process.wait_for_completion(check_interval=5)
        download = process.download()
        with open(convert_filename, "wb") as f:
            f.write(download.read())


    def execute(self):
        result = {}
        args = web.input()
        logger.info(u'入参:%s' %args)

        try:
            book_data = args.get('bookData')
            # 处理数据
            data = base64.b64decode(book_data)#.split(':')[1]
            data_json = json.loads(data)
            data_posts = data_json.get('posts')[0]

            # 创建HTML
            book_title = str(data_posts.get('title')).strip() 
            book_subtitle = str(data_posts.get('subtitle'))
            book_author = str(data_posts.get('orig_author'))
            page = HTML(book_title, book_subtitle, book_author)
            filename = page.create(data_json, data_posts.get('contents'))

            # 转换文件
            convert_filename = '%s.mobi' %book_title
            self.convert(filename, convert_filename)

            # 发送邮件
            mail = SendMail()
            mail.send(convert_filename, 'jacksyen@kindle.com', book_title, book_author)
            mail.close()

            result['status'] = 'SUCCESS'
            result['msg'] = u'推送成功，请稍侯查看您的kindle'
        except Exception, err:
            result['status'] = 'ABNORMAL'
            result['msg'] = u'推送异常,%s，请联系:hyqiu.syen@gmail.com' %err
        logger.info(u'出参：%s' %str(result))
        return json.dumps(result)


if __name__ == "__main__":
    logger.info(u'-----------系统启动-----------')
    # 设置系统编码
    reload(sys)
    sys.setdefaultencoding('utf-8')
    web.wsgi.runwsgi = lambda func, addr=None: web.wsgi.runfcgi(func, addr)   ##这行是新增的
    app.run()
