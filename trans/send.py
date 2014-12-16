# -*- coding: utf-8 -*-

import web
import json
import base64
import uuid

from sync import SyncThread
from helper.log import logger
from helper.dbase import SQLite
from helper.mail import SendMail
from helper.page import HTML
import helper.aop as aop
from helper.decrypt import decrypt
from db.tbl_wait_htmls import Tbl_Wait_Htmls
from db.tbl_wait_emails import Tbl_Wait_Emails

class Send:

    def __init__(self):
        self.conn = SQLite.conn()
        self.db = self.conn.cursor()

    def __del__(self):
        if self.conn:
            SQLite.close(self.conn)

    def GET(self):
        return self.execute(web.input())

    def POST(self):
        return self.execute(web.input())

    @aop.exec_time
    def execute(self, args):
        result = {}
        try:
            # 图书数据
            book_data = args.get('bookData')
            # 推送的email地址
            to_email = args.get('toMail')

            # 请求ID
            request_id = '%s_%s' %(to_email, str(uuid.uuid1()))
            logger.info(u'请求开始，ID:%s', request_id)

            # 处理数据
            data = decrypt.parse(book_data)
            data_json = json.loads(data)
            data_posts = data_json.get('posts')[0]

            # 创建HTML
            book_title = str(data_posts.get('title')).strip()
            book_subtitle = str(data_posts.get('subtitle'))
            book_author = str(data_posts.get('orig_author'))
            page = HTML(book_title, book_subtitle, book_author)
            book_html_path = page.create(data_json, data_posts.get('contents'))

            # 将待转换的书籍html信息存储在数据库中
            wait_htmls = Tbl_Wait_Htmls()
            wait_htmls.add(request_id, book_html_path)

            # 将待发送邮件存储至数据库
            wait_emails = Tbl_Wait_Emails()
            wait_emails.add(request_id, to_email, book_title, book_author)

            # 开启异步进程，转换书籍并发送邮件
            thread = SyncThread(request_id, book_author)
            #thread.start()

            result['status'] = 'SUCCESS'
            result['msg'] = u'推送成功，请稍侯查看您的kindle'
        except Exception, err:
            result['status'] = 'ABNORMAL'
            result['msg'] = u'推送异常,%s，请联系:hyqiu.syen@gmail.com' %err
        return json.dumps(result)
