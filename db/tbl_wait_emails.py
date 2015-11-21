#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
author by jacksyen[hyqiu.syen@gmail.com]
---------------------------------------
等待发送邮件操作
"""

from helper.dbase import MySQL
from helper.util import DateUtil
import helper.aop as aop
import webglobal.globals as gk7

class Tbl_Wait_Emails:

    def __init__(self):
        self.conn = MySQL.conn()
        self.cur = self.conn.cursor()

    def __del__(self):
        if self.conn:
            MySQL.close(self.conn)
    '''
    将信息添加至待发送邮件数据表
    email_id: 待发送邮件Id
    tomail: 发送到的email
    title: 标题
    author: 作者
    '''
    @aop.exec_time
    def add(self, email_id, tomail, title, auth):
        self.cur.execute('''INSERT INTO gk7_douban_wait_emails(email_id, email_to_user, email_title, email_auth, email_send_status, addtime) VALUES (%s, %s, %s, %s, %s, %s)''', (email_id, tomail, title, auth, gk7.STATUS.get('wait'), DateUtil.getDate(format='%Y-%m-%d %H:%M:%S')))
        self.conn.commit()

    '''
    将信息添加至待发送邮件数据表
    email_id: 待发送邮件Id
    tomail: 发送到的email
    title: 标题
    author: 作者
    attach_file: 附件
    '''
    @aop.exec_time
    def add_full(self, email_id, tomail, title, auth, attach_file):
        self.cur.execute('''INSERT INTO gk7_douban_wait_emails(email_id, email_to_user, email_attach_file, email_title, email_auth, email_send_status, addtime) VALUES (%s, %s, %s, %s, %s, %s, %s)''', (email_id, tomail, attach_file, title, auth, gk7.STATUS.get('wait'), DateUtil.getDate(format='%Y-%m-%d %H:%M:%S')))
        self.conn.commit()
        

    '''
    根据请求ID获取待发送邮件信息
    request_id: 请求ID
    '''
    @aop.exec_time
    def get(self, email_id):
        self.cur.execute('''SELECT email_id, email_to_user, email_attach_file, email_title, email_auth, email_send_status FROM gk7_douban_wait_emails WHERE email_id =%s''', (email_id, ))
        return self.cur.fetchone()

    '''
    根据请求ID修改发送邮件状态
    email_id: 邮件ID
    send_status: 发送状态
    '''
    @aop.exec_time
    def update_status(self, email_id, send_status):
        self.cur.execute('''UPDATE gk7_douban_wait_emails SET email_send_status = %s WHERE email_id = %s''', (send_status, email_id))
        self.conn.commit()

    '''
    根据邮件ID修改待发送邮件附件信息
    email_id: 邮件ID
    attach_file: 附件
    '''
    @aop.exec_time
    def update_attach_file(self, email_id, attach_file):
        self.cur.execute('''UPDATE gk7_douban_wait_emails SET email_attach_file = %s WHERE email_id = %s''', (attach_file, email_id))
        self.conn.commit()
