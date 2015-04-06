#-*- coding:utf-8 -*-

'''
数据库连接池
'''

import MySQLdb
from MySQLdb import cursors
from DBUtils.PooledDB import PooledDB

import webglobal.globals as gk7

class MySQL:

    # 初始化连接池
    pool = PooledDB(MySQLdb, 3, host=gk7.DB_CONFIG.get('host'), user=gk7.DB_CONFIG.get('user'), passwd=gk7.DB_CONFIG.get('passwd'), db=gk7.DB_CONFIG.get('db'), port=gk7.DB_CONFIG.get('port'), charset='UTF8', cursorclass=cursors.DictCursor)

    def __init__(self):
        pass

    @staticmethod
    def conn():
        conn = MySQL.pool.connection()
        return conn

    @staticmethod
    def close(conn):
        if conn:
            conn.close()
