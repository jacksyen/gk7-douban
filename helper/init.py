#!/usr/bin/env python
# -*- coding: utf-8 -*-


# init.py --- 
# 
# Filename: init.py
# Description: 
# Author: jacksyen
# Maintainer: 
# Created: 三 12月 10 22:37:17 2014 (+0800)
# Version: 
# Package-Requires: ()
# Last-Updated: 周四 十二月 11 11:03:43 2014 (+0800)
#           By: Administrator
#     Update #: 17
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
from dbase import SQLite
from util import DateUtil
from db.create_table import Create
from db.tbl_globals import Tbl_Global
from webglobal.globals import Global

# Code:
class Init_DB:

    @staticmethod
    def init():
        conn = SQLite.conn()
        cursor = conn.cursor()
        ## 创建全局配置表
        cursor.execute(Create.gk7_douban_global())
        ## 创建书籍表
        cursor.execute(Create.gk7_douban_books())
        ## 书籍待转换表
        cursor.execute(Create.gk7_douban_wait_htmls())
        ## 创建等待发送邮件表
        cursor.execute(Create.gk7_douban_wait_emails())
        conn.commit()
        SQLite.close(conn)

        ## 初始化全局配置表
        tbl_global = Tbl_Global()
        tbl_global.check_init()


# 
# init.py ends here
