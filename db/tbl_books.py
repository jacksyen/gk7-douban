#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
author by jacksyen[hyqiu.syen@gmail.com]
---------------------------------------
书籍数据库操作
"""
# tbl_books.py --- 
# 
# Filename: tbl_books.py
# Description: 
# Author: jacksyen
# Maintainer: 
# Created: 六 12月 13 11:06:21 2014 (+0800)
# Version: 
# Package-Requires: ()
# Last-Updated: 六 12月 13 11:24:14 2014 (+0800)
#           By: jacksyen
#     Update #: 9
# URL: 
# Doc URL: 
# Keywords: 
# Compatibility: 
# 
# 

# Commentary: 
# 
# 
# 
# 

# Change Log:
# 
# 
# 
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.
# 
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with GNU Emacs.  If not, see <http://www.gnu.org/licenses/>.
# 
# 

# Code:
class tbl_books:

    def __init__(self):
        self.conn = SQLite.conn()
        self.db = self.conn.cursor()

    def __del__(self):
        if self.conn:
            SQLite.close(self.conn)

    '''
    添加书籍信息
    request_id: 请求ID
    
    '''
    def add(self, request_id, book_title, book_subtitle, book_auth):
        self.db.execute('INSERT INTO %s(request_id, book_title, book_subtitle, book_author, addtime, updatetime) VALUES (?, ?, ?, ?, ?, ?, ?)' %Global.GLOBAL_DB_TBL_BOOK_NAME, request_id, booke_title, book_subtitle, book_auth, DateUtil.getDate(format='%Y-%m-%d %H:%M:%S'), DateUtil.getDate(format='%Y-%m-%d %H:%M:%S'))
        self.conn.commit()


# 
# tbl_books.py ends here
