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

    '''
    根据请求ID获取待发送邮件信息
    request_id: 请求ID
    '''
    def get(self, request_id):
        self.db.execute('SELECT email_to_user, email_attach_file, email_title, email_auth, email_send_status, addtime, updatetime FROM %s WHERE request_id ="%s"' %(Global.GLOBAL_DB_TBL_WAIT_EMAILS_NAME, request_id))
        return self.db.fetchone()

    '''
    根据请求ID修改发送邮件状态
    request_id: 请求ID
    send_status: 发送状态
    '''
    def update_status(self, request_id, send_status):
        self.db.execute('UPDATE %s SET email_send_status = ?, updatetime = ? WHERE request_id = ?' %(Global.GLOBAL_DB_TBL_WAIT_EMAILS_NAME), (send_status, DateUtil.getDate(format='%Y-%m-%d %H:%M:%S'), request_id))
        self.conn.commit()

    '''
    根据请求ID修改待发送邮件附件信息
    request_id: 请求ID
    attach_file: 发送状态
    '''
    def update_attach_file(self, request_id, attach_file):
        self.db.execute('UPDATE %s SET email_attach_file = ?, updatetime = ? WHERE request_id = ?' %(Global.GLOBAL_DB_TBL_WAIT_EMAILS_NAME), (attach_file, DateUtil.getDate(format='%Y-%m-%d %H:%M:%S'), request_id))
        self.conn.commit()
