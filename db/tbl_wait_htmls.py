#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
author by jacksyen[hyqiu.syen@gmail.com]
---------------------------------------
书籍html待转换表操作
"""
import uuid
from helper.dbase import SQLite
from helper.util import DateUtil
import helper.aop as aop
import webglobal.globals as gk7

class Tbl_Wait_Htmls:

    def __init__(self):
        self.conn = SQLite.conn()
        self.db = self.conn.cursor()

    def __del__(self):
        if self.conn:
            SQLite.close(self.conn)

    '''
    增加转换信息
    request_id: 请求id
    book_html_path: 书籍html绝对路径
    '''
    @aop.exec_time
    def add(self, request_id, book_html_path):
        self.db.execute('''INSERT INTO %s(book_convert_id, request_id , book_html_path, book_convert_status, addtime, updatetime) VALUES(?, ?, ?, ?, ?, ?)''' %(gk7.TABLE_NAMES.get('wait_htmls')), (str(uuid.uuid1()), request_id, book_html_path, gk7.STATUS.get('wait'), DateUtil.getDate(format='%Y-%m-%d %H:%M:%S'), DateUtil.getDate(format='%Y-%m-%d %H:%M:%S')))
        self.conn.commit()

    '''
    根据请求ID获取待转换书籍信息
    request_id: 请求ID
    '''
    @aop.exec_time
    def get(self, request_id):
        self.db.execute('''SELECT book_convert_id, book_html_path FROM %s WHERE request_id = ?''' %(gk7.TABLE_NAMES.get('wait_htmls')), (request_id, ))
        return self.db.fetchone()

    '''
    根据请求ID更新书籍转换状态,添加书籍转换完成的绝对路径
    status: 转换状态
    request_id: 请求ID
    '''
    @aop.exec_time
    def update_status(self, status, request_id, book_convert_path=None):
        self.db.execute('''UPDATE %s SET book_convert_status = ?, book_convert_path = ?, updatetime = ? WHERE request_id =?''' %(gk7.TABLE_NAMES.get('wait_htmls')), (status, book_convert_path, DateUtil.getDate(format='%Y-%m-%d %H:%M:%S'), request_id))
        self.conn.commit()
