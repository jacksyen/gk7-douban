#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
author by jacksyen[hyqiu.syen@gmail.com]
---------------------------------------
书籍数据库操作
"""
import helper.aop as aop
from helper.dbase import SQLite
from helper.util import DateUtil, RandomUtil
import webglobal.globals as gk7

class Tbl_Books:

    def __init__(self):
        self.conn = SQLite.conn()
        self.db = self.conn.cursor()

    def __del__(self):
        if self.conn:
            SQLite.close(self.conn)

    '''
    添加书籍信息
    返回书籍ID，即book_id
    
    book_number: 书籍号码(格式：作者ID_书名标题)
    book_title: 标题
    book_subtitle: 副标题
    book_author: 作者
    book_size: 书籍大小(客户端传递的bookData大小，即豆瓣文章加密字符串大小)
    '''
    @aop.exec_time
    def add(self, book_number, book_title, book_subtitle, book_author, book_size):
        book_id = RandomUtil.random32Str()
        self.db.execute('INSERT INTO %s(book_id, book_number, book_title, book_subtitle, book_author, book_size, addtime, updatetime) VALUES ("%s", "%s", "%s", "%s", "%s", %d, "%s", "%s")' %(gk7.TABLE_NAMES.get('book'), book_id, book_number, book_title, book_subtitle, book_author, book_size, DateUtil.getDate(format='%Y-%m-%d %H:%M:%S'), DateUtil.getDate(format='%Y-%m-%d %H:%M:%S')))
        self.conn.commit()
        return book_id

    '''
    根据书籍号码和书籍大小查询书籍信息
    book_number: 书籍号码(格式：作者ID_书名标题)
    book_size: 书籍大小(客户端传递的bookData大小，即豆瓣文章加密字符串大小)
    '''
    @aop.exec_time
    def get(self, book_number, book_size):
        self.db.execute('SELECT book_id, book_title, book_subtitle, book_author, book_file_path, addtime, updatetime FROM %s WHERE book_number ="%s" AND book_size = %d AND book_file_path !=""' %(gk7.TABLE_NAMES.get('book'), book_number, book_size))
        return self.db.fetchone()

    '''
    根据书籍ID查询书籍信息
    book_id: 书籍ID
    '''
    @aop.exec_time
    def get_by_book_id(self, book_id):
        self.db.execute('SELECT book_number, book_title, book_subtitle, book_author, book_file_path, book_size, book_cover, addtime, updatetime FROM %s WHERE book_id ="%s"' %(gk7.TABLE_NAMES.get('book'), book_id))
        return self.db.fetchone()

    '''
    根据书籍号码修改书籍文件路径
    book_id: 书籍ID
    book_file_path: 书籍文件路径(绝对路径)
    '''
    @aop.exec_time
    def update_file_path(self, book_id, book_file_path):
        self.db.execute('UPDATE %s SET book_file_path = "%s", updatetime = "%s" WHERE book_id = "%s"' %(gk7.TABLE_NAMES.get('book'), book_file_path, DateUtil.getDate(format='%Y-%m-%d %H:%M:%S'), book_id))
        self.conn.commit()

    '''
    更新书籍封面
    book_id: 书籍ID
    book_cover_path: 书籍封面路径
    '''
    @aop.exec_time
    def update_cover(self, book_id, book_cover_path):
        self.db.execute('UPDATE %s SET book_cover = "%s", updatetime = "%s" WHERE book_id = "%s"' %(gk7.TABLE_NAMES.get('book'), book_cover_path, DateUtil.getDate(format='%Y-%m-%d %H:%M:%S'), book_id))
        self.conn.commit()

