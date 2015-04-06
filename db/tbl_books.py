#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
author by jacksyen[hyqiu.syen@gmail.com]
---------------------------------------
书籍数据库操作
"""
import helper.aop as aop
from helper.dbase import MySQL
from helper.util import DateUtil, RandomUtil
import webglobal.globals as gk7

class Tbl_Books:

    def __init__(self):
        self.conn = MySQL.conn()
        self.cur = self.conn.cursor()

    def __del__(self):
        if self.conn:
            MySQL.close(self.conn)

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
    def add(self, book_id, ebook_id, book_title, book_subtitle, book_author, book_size, book_cover_remote_path):
        self.cur.execute('''INSERT INTO gk7_douban_books(id, ebook_id, book_title, book_subtitle, book_author, book_size, book_cover_remote_path, addtime) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)''', (book_id, ebook_id, book_title, book_subtitle, book_author, book_size, book_cover_remote_path, DateUtil.getDate(format='%Y-%m-%d %H:%M:%S')))
        self.conn.commit()

    '''
    根据书籍号码和书籍大小查询书籍信息
    ebook_id: 书籍号码(对应douban书籍ID)
    book_size: 书籍大小(客户端传递的bookData大小，即豆瓣文章加密字符串大小)
    '''
    @aop.exec_time
    def get(self, ebook_id, book_size):
        self.cur.execute('''SELECT id, ebook_id, book_title, book_subtitle, book_author, book_file_path, addtime, updatetime FROM gk7_douban_books WHERE ebook_id =%s AND book_size = %s AND book_file_path !=""''', (ebook_id, book_size))
        return self.cur.fetchone()

    '''
    根据书籍ID查询书籍信息
    book_id: 书籍ID
    '''
    @aop.exec_time
    def get_by_book_id(self, book_id):
        self.cur.execute('''SELECT id, ebook_id, book_title, book_subtitle, book_author, book_file_path, book_size, book_cover_local_path FROM gk7_douban_books WHERE id =%s''', (book_id, ))
        return self.cur.fetchone()

    '''
    根据书籍号码修改书籍文件路径
    book_id: 书籍ID
    book_file_path: 书籍文件路径(绝对路径)
    '''
    @aop.exec_time
    def update_file_path(self, book_id, book_file_path):
        self.cur.execute('''UPDATE gk7_douban_books SET book_file_path = %s WHERE id = %s''', (book_file_path, book_id))
        self.conn.commit()

    '''
    更新书籍封面
    book_id: 书籍ID
    book_cover_path: 书籍封面路径
    '''
    @aop.exec_time
    def update_cover(self, book_id, book_cover_local_path):
        self.cur.execute('''UPDATE gk7_douban_books SET book_cover_local_path = %s WHERE id = %s''', (book_cover_local_path, book_id))
        self.conn.commit()

