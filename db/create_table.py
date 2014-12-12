#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
author by jacksyen[hyqiu.syen@gmail.com]
---------------------------------------
创建数据库表信息（如果不存在）
"""
from webglobal.globals import Global

class Create:

    def __init__(self):
        pass

    '''
    获取全局配置表sql
    '''
    @staticmethod
    def gk7_douban_global():
        return 'CREATE TABLE IF NOT EXISTS %s(smtp text, smtp_port text, email_user text, email_pwd text, email_encode text, addtime datetime, updatetime datetime)' %(Global.GLOBAL_DB_TBL_GLOBAL_NAME)

    '''
    获取等待发送邮件表sql
    email_send_status: 邮件发送状态[WAIT:等待发送, COMPLETE:发送完成, ERROR:发送异常]
    '''
    @staticmethod
    def gk7_douban_wait_emails():
        return 'CREATE TABLE IF NOT EXISTS %s(email_to_user text, email_attach_file text, email_title text, email_auth text, email_send_status text, request_id text, addtime datetime, updatetime datetime)' %(Global.GLOBAL_DB_TBL_WAIT_EMAILS_NAME)

    '''
    获取所有书籍表sql
    book_number: 书籍id
    book_convert_id: 书籍原始转换id
    book_title: 标题
    '''
    @staticmethod
    def gk7_douban_books():
        return 'CREATE TABLE IF NOT EXISTS %s(book_number text, book_convert_id text, book_title text, book_subtitle text, book_author text, book_file_path text, addtime datetime, updatetime datetime)' %(Global.GLOBAL_DB_TBL_BOOK_NAME)

    '''
    书籍html等待转换表
    '''
    @staticmethod
    def gk7_douban_wait_htmls():
        return 'CREATE TABLE IF NOT EXISTS %s(book_convert_id text, request_id text, book_html_path text, book_convert_path text, book_convert_status text, addtime datetime, updatetime datetime)' %(Global.GLOBAL_DB_TBL_WAIT_HTMLS)
