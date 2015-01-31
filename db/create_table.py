#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
author by jacksyen[hyqiu.syen@gmail.com]
---------------------------------------
创建数据库表信息（如果不存在）

|Table: gk7_douban_wait_emails
|--------------------------
| Column_name        Datatype    Pk    Description
| email_to_user      text              待发送邮箱
| email_attach_file  text
| email_user         text              邮箱用户地址
| email_pwd          text              邮箱用户密码
| email_encode       text              邮件编码
| addtime            datetime          增加日期
| updatetime         datetime          更新日期
--------------------------------------------
"""
import webglobal.globals as gk7

class Create:

    def __init__(self):
        pass

    '''
    获取等待发送邮件表sql
    email_send_status: 邮件发送状态[WAIT:等待发送, COMPLETE:发送完成, ERROR:发送异常]
    '''
    @staticmethod
    def gk7_douban_wait_emails():
        return 'CREATE TABLE IF NOT EXISTS %s(email_to_user text, email_attach_file text, email_title text, email_auth text, email_send_status text, request_id text, addtime datetime, updatetime datetime)' %(gk7.TABLE_NAMES.get('wait_emails'))

    '''
    获取所有书籍表sql
    其中book_number + book_size 做主键，不能重复

    book_id: 书籍ID（主键）
    book_number: (格式：作者ID_书名标题)
    book_title: 标题
    book_subtitle: 副标题
    book_author: 作者
    book_file_path: 书籍绝对路径(转换后的)
    book_size: 书籍大小
    book_cover: 书籍封面本地路径
    addtime: 添加时间
    updatetime: 更新时间
    '''
    @staticmethod
    def gk7_douban_books():
        return 'CREATE TABLE IF NOT EXISTS %s(book_id text PRIMARY KEY, book_number text, book_title text, book_subtitle text, book_author text, book_file_path text, book_size INTEGER, book_cover text, addtime datetime, updatetime datetime)' %(gk7.TABLE_NAMES.get('book'))

    '''
    获取书籍关联的图片路径表SQL
    book_id: 书籍ID
    book_images_local_path: 书籍图片本地路径集合
    book_images_remote_path: 书籍图片远程路径集合
    addtime: 添加时间
    updatetime: 更新时间
    '''
    @staticmethod
    def gk7_douban_book_img():
        return 'CREATE TABLE IF NOT EXISTS %s(book_id text PRIMARY KEY, book_images_local_path text, book_images_remote_path text, addtime datetime, updatetime datetime)' %(gk7.TABLE_NAMES.get('book_img'))

    '''
    书籍html等待转换表
    '''
    @staticmethod
    def gk7_douban_wait_htmls():
        return 'CREATE TABLE IF NOT EXISTS %s(book_convert_id text, request_id text, book_html_path text, book_convert_path text, book_convert_status text, addtime datetime, updatetime datetime)' %(gk7.TABLE_NAMES.get('wait_htmls'))
