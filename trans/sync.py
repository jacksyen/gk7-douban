#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
author by jacksyen[hyqiu.syen@gmail.com]
---------------------------------------
异步线程
[转换书籍, 发送邮件]
"""
import threading

from helper.log import logger
from helper.mail import SendMail
from helper.proc import proc_helper
from webglobal.globals import Global, Global_Status
from db.tbl_wait_htmls import Tbl_Wait_Htmls
from db.tbl_wait_emails import Tbl_Wait_Emails

class SyncThread(threading.Thread):

    '''
    request_id: 请求ID
    '''
    def __init__(self, request_id):
        threading.Thread.__init__(self)
        self.request_id = request_id

    def run(self):
        # 读取待转换的书籍信息
        wait_html = Tbl_Wait_Htmls()
        wait_html_info = wait_html.get(self.request_id)
        if wait_html_info == None:
            logger.error(u'未找到待转换的书籍信息，请求ID：%s', self.request_id)
            exit(-1)

        ## 调用转换功能
        out_file_path = proc_helper.convert(wait_html_info['book_html_path'], Global.GLOBAL_OUT_DATA_DIRS)
        print out_file_path
        if out_file_path == None:
            # 转换失败
            logger.error(u'转换失败，请求ID：%s', self.request_id)
            wait_html.update_status(Global_Status.ERROR, self.request_id)
            exit(-1)
        
        # 转换成功，修改状态，添加书籍输出路径
        wait_html.update_status(Global_Status.COMPLETE, self.request_id, out_file_path)

        wait_email = Tbl_Wait_Emails()
        # 修改待发送邮件附件信息
        wait_email.update_attach_file(self.request_id, out_file_path)
        # 读取待发送邮件信息
        wait_email_info = wait_email.get(self.request_id)
        if wait_email_info == None:
            logger.error(u'未找到待发送邮件信息，请求ID:%s', self.request_id)
            exit(-1)

        # 发送邮件
        mail = SendMail()
        send_request = mail.send(wait_email_info['email_attach_file'], str(wait_email_info['email_to_user']), str(wait_email_info['email_title']), str(wait_email_info['email_auth']))

        # 修改待发送邮件信息状态
        if send_request:
            ## 发送成功
            wait_email.update_status(self.request_id, Global_Status.COMPLETE)
        else:
            ## 发送失败
            wait_email.update_status(self.request_id, Global_Status.ERROR)
