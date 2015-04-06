#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
author by jacksyen[hyqiu.syen@gmail.com]
---------------------------------------
书籍html待转换表操作
"""
import uuid
from helper.dbase import MySQL
from helper.util import DateUtil
import helper.aop as aop
import webglobal.globals as gk7

class Tbl_Wait_Converts:

    def __init__(self):
        self.conn = MySQL.conn()
        self.cur = self.conn.cursor()

    def __del__(self):
        if self.conn:
            MySQL.close(self.conn)

    '''
    增加转换信息
    convert_id: 转换id
    request_user: 请求用户
    book_html_local_path: 书籍html本地路径
    '''
    @aop.exec_time
    def add(self, convert_id, request_user, book_html_local_path):
        self.cur.execute('''INSERT INTO gk7_douban_wait_converts(convert_id, request_user, book_html_local_path, convert_status, addtime) VALUES(%s, %s, %s, %s, %s)''', (convert_id, request_user, book_html_local_path, gk7.STATUS.get('wait'), DateUtil.getDate(format='%Y-%m-%d %H:%M:%S')))
        self.conn.commit()

    '''
    根据转换ID获取待转换书籍信息
    convert_id: 转换ID
    '''
    @aop.exec_time
    def get(self, convert_id):
        self.cur.execute('''SELECT convert_id, book_html_local_path, book_convert_file_path FROM gk7_douban_wait_converts WHERE convert_id = %s''', (convert_id, ))
        return self.cur.fetchone()

    '''
    根据请求ID更新书籍转换状态,添加书籍转换完成的绝对路径
    status: 转换状态
    convert_id: 请求ID
    '''
    @aop.exec_time
    def update_status(self, status, convert_id, book_convert_path=None):
        self.cur.execute('''UPDATE gk7_douban_wait_converts SET convert_status = %s, book_convert_file_path = %s WHERE convert_id =%s''', (status, book_convert_path, convert_id))
        self.conn.commit()
