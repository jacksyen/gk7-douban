# -*- coding: utf-8 -*-

import web
import json
import base64
import uuid
import weakref

from sync import SyncThread
from sync import SyncSendMail
from helper.log import logger
from helper.dbase import SQLite
from helper.mail import SendMail
from helper.page import HTML
import helper.aop as aop
from helper.decrypt import decrypt
from db.tbl_wait_htmls import Tbl_Wait_Htmls
from db.tbl_wait_emails import Tbl_Wait_Emails
from db.tbl_books import Tbl_Books
from db.tbl_book_img import Tbl_Book_Img
from webglobal.globals import Global


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

    @aop.exec_out_time
    def execute(self, args):
        try:
            # 图书数据
            book_data = args.get('bookData')
            # 推送的email地址
            to_email = args.get('toMail')
            if not book_data or not to_email:
                return json.dumps({'status': 'WARN', 'msg': u'参数不能为空，请联系:hyqiu.syen@gmail.com'})
            # 请求ID
            request_id = '%s_%s' %(to_email, str(uuid.uuid1()))
            # 处理数据
            data = decrypt.parse(book_data)
            data_json = json.loads(data)
            data_posts = data_json.get('posts')[0]

            # 图书标题
            book_title = str(data_posts.get('title')).strip()
            # 图书副标题
            book_subtitle = str(data_posts.get('subtitle'))
            # 图书作者
            book_author = str(data_posts.get('orig_author'))
            # 图书译者
            book_translator = str(data_posts.get('translator'))

            # 将待发送邮件存储至数据库
            wait_emails = Tbl_Wait_Emails()
            wait_emails.add(request_id, to_email, book_title, book_author)

            # 书籍number
            book_number = '%s_%s' %(str(data_json.get('authorId')), book_title)
            # 书籍大小
            book_size = len(book_data)

            # 判断书籍是否存在数据库中
            books = Tbl_Books()
            book_info = books.get(book_number, book_size)
            # 如果书籍已经存在
            if book_info:
                # 修改待发送邮件附件信息
                attach_file = str(book_info['book_file_path'])
                # 如果不为空直接发送邮件
                if attach_file:
                    wait_emails.update_attach_file(request_id, attach_file)
                    # 发送邮件并修改待发送邮件状态
                    send_mail = SyncSendMail()
                    send_mail.send(request_id, attach_file, to_email, book_title, book_author)
                    return json.dumps({'status': 'SUCCESS', 'msg': u'推送成功，请稍侯查看您的kindle'})

            # 创建HTML
            # 源文件目录[绝对路径](格式：主目录/作者/书名标题/书籍大小)
            file_dir = '%s/%s/%s/%s' %(Global.GLOBAL_DATA_DIRS, book_author, book_title, str(book_size))
            page = HTML(book_title, book_subtitle, book_author, file_dir, book_translator)
            book_html_path, book_images_remote_path = page.create(data_posts.get('contents'))

            # 存储书籍信息
            book_id = books.add(book_number, book_title, book_subtitle, book_author, book_size)
            # 存储书籍图片路径信息
            if len(book_images_remote_path):
                book_img = Tbl_Book_Img()
                book_img.add(book_id, book_images_remote_path)

            # 将待转换的书籍html信息存储在数据库中
            wait_htmls = Tbl_Wait_Htmls()
            wait_htmls.add(request_id, book_html_path)

            # 开启异步进程，转换书籍并发送邮件
            # 书籍输出目录[OUT_DATA_DIRS/书名标题/大小/]
            out_file_dir = '%s/%s/%s/%s' %(Global.GLOBAL_OUT_DATA_DIRS, book_author, book_title, str(book_size))
            thread = SyncThread(request_id, book_author, book_id, file_dir, out_file_dir)
            thread._children = weakref.WeakKeyDictionary()
            thread.start()
            if len(book_images_remote_path):
                return json.dumps({'status': 'SUCCESS', 'msg': u'推送成功，书籍中存在图片，推送的时间更长一些，请稍侯查看您的kindle'})
            return json.dumps({'status': 'SUCCESS', 'msg': u'推送成功，请稍侯查看您的kindle'})
        except Exception, err:
            logger.error(u'推送异常,错误信息：%s，入参：%s' %(err, str(args)))
            return json.dumps({'status': 'ABNORMAL', 'msg': u'推送异常,%s，请联系:hyqiu.syen@gmail.com' %err})
