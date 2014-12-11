#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
author by jacksyen[hyqiu.syen@gmail.com]
---------------------------------------
等待发送邮件操作
"""

from helper.dbase import SQLite
from helper.util import DateUtil
from webglobal.globals import Global, Global_Status

class Tbl_Wait_Emails:

    def __init__(self):
        self.conn = SQLite.conn()
        self.db = self.conn.cursor()

    def __del__(self):
        if self.conn:
            SQLite.close(self.conn)
    '''
    将信息添加至待发送邮件数据表
    filename: 附件名
    tomail: 发送到的email
    title: 标题
    author: 头部作者
    '''
    def add(self, request_id, tomail, title, auth):
        self.db.execute('INSERT INTO %s(email_to_user, email_title, email_auth, email_send_status, request_id, addtime, updatetime) VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s")' %(Global.GLOBAL_DB_TBL_WAIT_EMAILS_NAME, tomail, title, auth, Global_Status.WAIT, request_id, DateUtil.getDate(format='%Y-%m-%d %H:%M:%S'), DateUtil.getDate(format='%Y-%m-%d %H:%M:%S')))
        self.conn.commit()
