#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
author by jacksyen[hyqiu.syen@gmail.com]
---------------------------------------
全局变量存储
"""
class Global:

    GLOBAL_DB_FILE = 'gk7-douban-read-send-kindle.db'

    GLOBAL_DB_TBL_BOOK_NAME = 'gk7_douban_books'

    GLOBAL_DB_TBL_GLOBAL_NAME = 'gk7_douban_global'

    GLOBAL_DB_TBL_WAIT_EMAILS_NAME = 'gk7_douban_wait_emails'


    ## email配置
    GLOBAL_EMAIL_SMTP = 'smtp.gmail.com'

    GLOBAL_EMAIL_SMTP_PORT = '25'

    GLOBAL_EMAIL_USER = 'hyqiu.syen@gmail.com'

    GLOBAL_EMAIL_PWD = 'Eva19898280'

    GLOBAL_EMAIL_ENCODE = 'utf-8'
    


    def __init__(self):
        pass

'''
邮件发送状态
'''
class Global_EMAILS_STATUS:

    WAIT = 'wait'

    COMPLETE = 'complete'

    ERROR = 'error'
