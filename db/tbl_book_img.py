#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
author by jacksyen[hyqiu.syen@gmail.com]
---------------------------------------
书籍图片路径数据库操作
"""
from webglobal.globals import Global
import helper.aop as aop
from helper.dbase import SQLite
from helper.util import DateUtil


class Tbl_Book_Img:

    def __init__(self):
        self.conn = SQLite.conn()
        self.db = self.conn.cursor()

    def __del__(self):
        if self.conn:
            SQLite.close(self.conn)

    '''
    添加书籍图片路径信息
    book_number: (格式：作者ID_书名标题)
    book_images_remote_path: (书籍图片远程路径)
    '''
    @aop.exec_time
    def add(self, book_number, book_images_remote_path):
        self.db.execute('INSERT INTO %s(book_number, book_images_remote_path, addtime, updatetime) VALUES ("%s", "%s", "%s", "%s")' %(Global.GLOBAL_DB_TBL_BOOK_IMG_NAME, book_number, Global.GLOBAL_DB_BOOK_IMG_PATH_SPLIT.join(book_images_remote_path), DateUtil.getDate(format='%Y-%m-%d %H:%M:%S'), DateUtil.getDate(format='%Y-%m-%d %H:%M:%S')))
        self.conn.commit()

    '''
    根据书籍ID获取图书的图片信息
    book_number: 书籍ID
    '''
    @aop.exec_time
    def get(self, book_number):
        self.db.execute('SELECT book_images_remote_path, addtime, updatetime FROM %s WHERE book_number ="%s"' %(Global.GLOBAL_DB_TBL_BOOK_IMG_NAME, book_number))
        return self.db.fetchone()

    '''
    根据书籍ID更新书籍本地图片
    book_number: 书籍ID
    book_images_local_path: 书籍本地图片集合
    '''
    @aop.exec_time
    def update_local_path(self, book_number, book_images_local_path):
        self.db.execute('UPDATE %s SET book_images_local_path = "%s", updatetime = "%s" WHERE book_number = "%s"' %(Global.GLOBAL_DB_TBL_BOOK_IMG_NAME, Global.GLOBAL_DB_BOOK_IMG_PATH_SPLIT.join(book_images_local_path), DateUtil.getDate(format='%Y-%m-%d %H:%M:%S'), book_number))
        self.conn.commit()
                        
