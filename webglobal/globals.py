#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
author by jacksyen[hyqiu.syen@gmail.com]
---------------------------------------
全局配置
"""
import os

# sqlite db name
DB_FILE = 'gk7-douban-read-send-kindle.db'

## 书籍信息表
TABLE_NAMES = {
    ## 书籍表
    'book': 'gk7_douban_books',
    ## 书籍图片路径表
    'book_img': 'gk7_douban_book_img',
    ## 全局配置表
    'global_name': 'gk7_douban_global',
    ## 等待发送邮件表
    'wait_emails': 'gk7_douban_wait_emails',
    ## 书籍html等待转换表
    'wait_htmls': 'gk7_douban_wait_htmls'
}

# 书籍封面前缀
BOOK_COVER_URL = 'http://img3.douban.com/view/ark_article_cover/retina/public/{}.jpg'

# 源文件存储目录
DATA_DIRS = '%s/data' %(os.path.abspath('.'))

BOOK_COVER_DIRS = '%s/cover' %(DATA_DIRS)

# 输出文件存储目录
OUT_DATA_DIRS = '%s/out-data' %(os.path.abspath('.'))

# 输出文件格式
OUT_FILE_FORMAT = 'mobi'

# 书籍图片路径分割字符
BOOK_IMG_PATH_SPLIT = ';'

# 书籍页面分隔符
BOOK_PAGE_SPLIT = 'pagebreak'

# email配置
EMAIL = {
    ## SMTP
    'smtp': 'smtp.gmail.com',
    ## 端口
    'port': 25,
    ## 发送方邮箱
    'user': 'hyqiu.syen@gmail.com',
    ## 发送方密码
    'pwd': '',
    ## 邮件编码
    'encode': 'UTF-8',
    ## 超时时间30秒
    'timeout': 30
}

'''
全局状态
+ 邮件表
+ htmls转换表
'''
STATUS = {
    'wait': 'wait',
    'complete': 'complete',
    'error': 'error'
}

## 日志存储目录
LOG_DIRS = '%s/logs' %(os.path.abspath('.'))
