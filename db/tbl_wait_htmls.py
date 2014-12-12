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
from webglobal.globals import Global, Global_Status

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
    def add(self, request_id, book_html_path):
        self.db.execute('INSERT INTO %s(book_convert_id, request_id , book_html_path, book_convert_status, addtime, updatetime) VALUES("%s", "%s", "%s", "%s", "%s", "%s")' %(Global.GLOBAL_DB_TBL_WAIT_HTMLS, str(uuid.uuid1()), request_id, book_html_path, Global_Status.WAIT, DateUtil.getDate(format='%Y-%m-%d %H:%M:%S'), DateUtil.getDate(format='%Y-%m-%d %H:%M:%S')))
        self.conn.commit()

    '''
    根据请求ID获取待转换书籍信息
    request_id: 请求ID
    '''
    def get(self, request_id):
        self.db.execute('SELECT book_convert_id, book_html_path FROM %s WHERE request_id = "%s"' %(Global.GLOBAL_DB_TBL_WAIT_HTMLS, request_id))
        return self.db.fetchone()

    '''
    根据请求ID更新书籍转换状态,添加书籍转换完成的绝对路径
    status: 转换状态
    request_id: 请求ID
    '''
    def update_status(self, status, request_id, book_convert_path=None):
        self.db.execute('UPDATE %s SET book_convert_status = "%s", book_convert_path = ?, updatetime = "%s" WHERE request_id ="%s"' %(Global.GLOBAL_DB_TBL_WAIT_HTMLS, status, DateUtil.getDate(format='%Y-%m-%d %H:%M:%S'), request_id), (book_convert_path,))
        self.conn.commit()
