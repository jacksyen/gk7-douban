#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
author by jacksyen[hyqiu.syen@gmail.com]
---------------------------------------
全局配置表操作
"""
from helper.dbase import SQLite
from helper.util import DateUtil
from webglobal.globals import Global

class Tbl_Global:

    def __init__(self):
        self.conn = SQLite.conn()
        self.db = self.conn.cursor()

    def __del__(self):
        if self.conn:
            SQLite.close(self.conn)

    def check_init(self):
        self.db.execute('SELECT * FROM %s' %Global.GLOBAL_DB_TBL_GLOBAL_NAME)
        result = self.db.fetchone()
        if result == None:
            self.db.execute('INSERT INTO %s(smtp, smtp_port, email_user, email_pwd, email_encode, addtime, updatetime) VALUES("%s", "%s", "%s", "%s", "%s", "%s", "%s")' %(Global.GLOBAL_DB_TBL_GLOBAL_NAME, Global.GLOBAL_EMAIL_SMTP, Global.GLOBAL_EMAIL_SMTP_PORT, Global.GLOBAL_EMAIL_USER, Global.GLOBAL_EMAIL_PWD, Global.GLOBAL_EMAIL_ENCODE, DateUtil.getDate(format='%Y-%m-%d %H:%M:%S'), DateUtil.getDate(format='%Y-%m-%d %H:%M:%S')))
