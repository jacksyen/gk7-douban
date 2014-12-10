# -*- coding:utf-8 -*-

import sqlite3 as db
from webglobal.globals import Global

class SQLite:

    def __init__(self):
        pass

    @staticmethod
    def conn():
        conn = db.connect(Global.GLOBAL_DB_FILE)
        conn.row_factory = db.Row
        return conn

    @staticmethod
    def close(conn):
        if conn:
            conn.close()
