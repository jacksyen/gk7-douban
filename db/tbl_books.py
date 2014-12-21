#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
author by jacksyen[hyqiu.syen@gmail.com]
---------------------------------------
书籍数据库操作
"""
import helper.aop as aop
from helper.dbase import SQLite
from helper.util import DateUtil
from webglobal.globals import Global


class Tbl_Books:

    def __init__(self):
        self.conn = SQLite.conn()
        self.db = self.conn.cursor()

    def __del__(self):
        if self.conn:
            SQLite.close(self.conn)

    '''
    添加书籍信息
    book_number: 书籍号码(格式：作者ID_书名标题)
    book_title: 标题
    book_subtitle: 副标题
    book_author: 作者
    '''
    @aop.exec_time
    def add(self, book_number, book_title, book_subtitle, book_author):
        self.db.execute('INSERT INTO %s(book_number, book_title, book_subtitle, book_author, addtime, updatetime) VALUES ("%s", "%s", "%s", "%s", "%s", "%s")' %(Global.GLOBAL_DB_TBL_BOOK_NAME, book_number, book_title, book_subtitle, book_author, DateUtil.getDate(format='%Y-%m-%d %H:%M:%S'), DateUtil.getDate(format='%Y-%m-%d %H:%M:%S')))
        self.conn.commit()

    '''
    根据书籍号码查询书籍信息
    book_number: 书籍号码(格式：作者ID_书名标题)
    '''
    @aop.exec_time
    def get(self, book_number):
        self.db.execute('SELECT book_title, book_subtitle, book_author, book_file_path, addtime, updatetime FROM %s WHERE book_number ="%s"' %(Global.GLOBAL_DB_TBL_BOOK_NAME, book_number))
        return self.db.fetchone()

    '''
    根据书籍号码修改书籍文件路径
    book_number: 书籍号码(格式：作者ID_书名标题)
    book_file_path: 书籍文件路径(绝对路径)
    '''
    @aop.exec_time
    def update_file_path(self, book_number, book_file_path):
        self.db.execute('UPDATE %s SET book_file_path = "%s", updatetime = "%s" WHERE book_number = "%s"' %(Global.GLOBAL_DB_TBL_BOOK_NAME, book_file_path, DateUtil.getDate(format='%Y-%m-%d %H:%M:%S'), book_number))
        self.conn.commit()
        
