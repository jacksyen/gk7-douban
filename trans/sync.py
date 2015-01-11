#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
author by jacksyen[hyqiu.syen@gmail.com]
---------------------------------------
异步线程
[转换书籍, 发送邮件]
"""
import sys
import threading

from helper.log import logger
from helper.mail import SendMail
from helper.proc import proc_helper
from helper.download import Files
import helper.aop as aop
from webglobal.globals import Global, Global_Status
from db.tbl_wait_htmls import Tbl_Wait_Htmls
from db.tbl_wait_emails import Tbl_Wait_Emails
from db.tbl_books import Tbl_Books
from db.tbl_book_img import Tbl_Book_Img

class SyncSendMail:
    
    def __init__(self):
        self.mail = SendMail()
        self.wait_email = Tbl_Wait_Emails()

    '''
    '''
    @aop.exec_time
    def send(self, request_id, attach_file, to_email, title, auth):
        send_request = self.mail.send(attach_file, to_email, title, auth)
        # 修改待发送邮件信息状态
        if send_request:
            ## 发送成功
            self.wait_email.update_status(request_id, Global_Status.COMPLETE)
            return
        ## 发送失败
        self.wait_email.update_status(request_id, Global_Status.ERROR)


class SyncThread(threading.Thread):

    '''
    request_id: 请求ID
    book_auth: 书籍作者
    book_id: 书籍ID
    out_dir: 书籍输出目录
    book_images_task: 书籍图片下载任务
    '''
    def __init__(self, request_id, book_author, book_id, out_dir, book_images_task):
        threading.Thread.__init__(self)
        self.request_id = request_id
        self.book_author = book_author
        self.book_id = book_id
        self.out_dir = out_dir
        self.book_images_task = book_images_task
    
    @aop.exec_time
    def run(self):
        try:
            # 读取待转换的书籍信息
            wait_html = Tbl_Wait_Htmls()
            wait_html_info = wait_html.get(self.request_id)
            if not wait_html_info:
                raise Exception, '未找到待转换的书籍信息'

            # 抓取书籍所需图片
            book_img = Tbl_Book_Img()
            book_img_info = book_img.get(self.book_id)
            if book_img_info:
                # 更新书籍所需图片表信息
                book_img.update_local_path(self.book_id, self.book_images_task.get())

            # 读取图书信息
            book = Tbl_Books()
            book_info = book.get_by_book_id(self.book_id)
            if not book_info:
                raise Exception, '获取图书信息失败，书籍ID：%s' %self.book_id

            ## 调用转换功能
            out_file_path = proc_helper.convert(str(wait_html_info['book_html_path']), self.out_dir, self.book_author)
            if out_file_path == None:
                # 转换失败
                wait_html.update_status(Global_Status.ERROR, self.request_id)
                raise Exception, '转换html to mobi失败'

            # 转换成功，修改状态，添加书籍输出路径
            wait_html.update_status(Global_Status.COMPLETE, self.request_id, out_file_path)
            # 修改书籍文件路径
            books = Tbl_Books()
            books.update_file_path(self.book_id, out_file_path)

            wait_email = Tbl_Wait_Emails()
            # 修改待发送邮件附件信息
            wait_email.update_attach_file(self.request_id, out_file_path)
            # 读取待发送邮件信息
            wait_email_info = wait_email.get(self.request_id)
            if not wait_email_info:
                raise Exception, '未找到待发送邮件信息，请求ID:%s' %self.request_id

            # 发送邮件
            send_mail = SyncSendMail()
            send_mail.send(self.request_id, wait_email_info['email_attach_file'], str(wait_email_info['email_to_user']), str(wait_email_info['email_title']), str(wait_email_info['email_auth']))
        except Exception, err:
            logger.error(u'异步线程出错，请求ID：%s，错误信息：%s', self.request_id, err)
            exit(-1)
