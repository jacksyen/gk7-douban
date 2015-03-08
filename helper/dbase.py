#-*- coding:utf-8 -*-

import sqlite3 as db
import webglobal.globals as gk7

class SQLite:

    def __init__(self):
        pass

    @staticmethod
    def conn():
        conn = db.connect(gk7.DB_FILE, timeout=20)
        conn.row_factory = db.Row
        # 处理中文， utf-8编码
        conn.text_factory = str
        return conn

    @staticmethod
    def close(conn):
        if conn:
            conn.close()
