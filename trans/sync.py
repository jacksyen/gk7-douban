#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
author by jacksyen[hyqiu.syen@gmail.com]
---------------------------------------
异步线程
[转换书籍, 发送邮件]
"""
import threading

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
        wait_htmls = Tbl_Wait_Htmls.get(self.request_id)
        if wait_htmls == None:
            pass
        ## 调用转换功能

        # 读取待发送邮件信息

        # 发送邮件
