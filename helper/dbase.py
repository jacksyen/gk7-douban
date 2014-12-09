# -*- coding:utf-8 -*-

import sqlite3 as db
from webglobal.global import Global
from util import DateUtil
from db.create_table import Create
from db.tbl_global import TBL_GLOBAL

class SQLite:

    @staticmethod
    def init():
        conn = SQLite.conn()
        cursor = conn.cursor()
        ## 创建全局配置表
        cursor.execute(Create.gk7_douban_global())
        ## 创建书籍表
        cursor.execute(Create.gk7_douban_books())
        ## 创建等待发送邮件表
        cursor.execute(Create.gk7_douban_wait_emails())
        conn.commit()
        SQLite.close(conn)

        ## 初始化全局配置表
        tbl_global = TBL_GLOBAL()
        tbl_global.check_init()


    @staticmethod
    def conn():
        conn = db.connect(Global.GLOBAL_DB_FILE)
        conn.row_factory = db.Row
        return conn

    @staticmethod
    def close(conn):
        if conn:
            conn.close()
