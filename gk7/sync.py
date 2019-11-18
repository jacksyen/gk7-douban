#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
author by jacksyen[hyqiu.syen@gmail.com]
---------------------------------------
异步线程
1. 抓取书籍所需图片（如果存在）
2. 转换书籍(html->mobi)
3. 发送邮件
"""
import threading

import globals
import util.aop as aop
from util.log import logger
from util.util import RandomUtil
from util.proc import proc_helper
from task.tasks import MailTask
from db.dbase import Database
from api import Api


class SyncThread(threading.Thread):

    '''
    convert_id: 转换ID
    email_id: 邮件ID
    book_id: 书籍ID
    out_dir: 书籍输出目录
    book_images_task: 书籍图片下载任务
    to_private_email: 用户个人邮箱
    '''
    def __init__(self, convert_id, email_id, book_id, out_dir, book_images_task, to_private_email):
        threading.Thread.__init__(self)
        self.convert_id = convert_id
        self.email_id = email_id
        self.book_id = book_id
        self.out_dir = out_dir
        self.book_images_task = book_images_task
        self.to_private_email = to_private_email
        self.db = Database()

    @aop.exec_time
    def run(self):
        try:
            # 读取待转换的书籍信息
            wait_converts_info = self.db.convert_get(self.convert_id)
            if not wait_converts_info:
                raise Exception(u'未找到待转换的书籍信息')

            # 读取书籍所需图片
            book_img_info = self.db.book_img_get(self.book_id)
            if book_img_info:
                # 更新书籍所需图片表信息
                self.db.book_img_update_local_path(self.book_id, self.book_images_task.get())

            # 读取书籍信息
            book_info = self.db.book_get_by_book_id(self.book_id)

            ## 调用转换功能
            out_file_path = proc_helper.convert(str(wait_converts_info['book_html_local_path']), self.out_dir, book_info['book_author'], book_info['book_cover_local_path'])
            if out_file_path == None:
                # 转换失败
                self.db.convert_update_status(globals.STATUS.get('error'), self.convert_id)
                raise Exception(u'rai转换html to mobi失败')

            # 转换成功，修改状态，添加书籍输出路径
            self.db.convert_update_status(globals.STATUS.get('complete'), self.convert_id, out_file_path)
            # 修改书籍文件路径
            self.db.book_update_file_path(self.book_id, out_file_path)

            # 修改待发送邮件附件信息
            self.db.email_update_attach_file(self.email_id, out_file_path)
            # 读取待发送邮件信息
            wait_email_info = self.db.email_get(self.email_id)
            if not wait_email_info:
                raise Exception(u'未找到待发送邮件信息，邮件ID:%s' %self.email_id)
            # 发送邮件
            Api.send_mail(self.email_id, wait_email_info['email_attach_file'], str(wait_email_info['email_to_user']), str(wait_email_info['email_title']), str(wait_email_info['email_auth']))
            # 发送邮件至个人邮箱to_private_email
            if self.to_private_email:
                private_email_id = RandomUtil.random32Str()
                self.db.email_add_full(private_email_id, self.to_private_email, str(wait_email_info['email_title']), str(wait_email_info['email_auth']), wait_email_info['email_attach_file'])
                MailTask.send.delay(private_email_id, wait_email_info['email_attach_file'], self.to_private_email, str(wait_email_info['email_title']), str(wait_email_info['email_auth']))
        except Exception as err:
            logger.error(u'异步线程出错，转换ID：%s，错误信息：%s', self.convert_id, err)
            exit(-1)
