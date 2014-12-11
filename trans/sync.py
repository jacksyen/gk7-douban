#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
author by jacksyen[hyqiu.syen@gmail.com]
---------------------------------------
异步线程
[转换书籍, 发送邮件]
"""
import threading

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
            pass # TODO 未找到信息

        ## 调用转换功能
        out_file_path = proc_helper.convert(wait_html_info['book_html_pah'], Global.GLOBAL_OUT_DATA_DIRS)
        if out_file_path == None:
            # 转换失败
            wait_html.update_status(Global_Status.ERROR, self.request_id)
            pass # TODO 直接assert
        
        # 转换成功，修改状态
        wait_html.update_status(Global_Status.COMPLETE, self.request_id)

        # 读取待发送邮件信息
        wait_email = Tbl_Wait_Emails()
        wait_email_info = wait_email.get(self.request_id)
        if wait_email_info == None:
            pass # TODO 未找到信息

        # 发送邮件
        
