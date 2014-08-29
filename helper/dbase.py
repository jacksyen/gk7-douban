# -*- coding:utf-8 -*-

import sqlite3 as db
#from webglobal import Global
from util import DateUtil

class SQLite:

    @staticmethod
    def init():
        """
        conn = SQLite.conn()
        conn.text_factory = str
        cursor = conn.cursor()
        SQLite.close(conn)
        """
        pass

    @staticmethod
    def conn():
        conn = db.connect('easylife.db')
        conn.row_factory = db.Row
        return conn

    @staticmethod
    def close(conn):
        if conn:
            conn.close()
