#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
author by jacksyen[hyqiu.syen@gmail.com]
---------------------------------------
全局配置
"""
import os

# 环境(DEV,TEST,ONLINE)
ENV = 'ONLINE'

DB_CONFIG = {
    'host': '192.168.1.66',
    'user': 'gk7',
    'passwd': 'gk7',
    'db': 'gk7_douban',
    'port': 3305
}

# 超时时间(s)
HTTP_TIME_OUT = 60

# 书籍封面前缀
BOOK_COVER_URL = 'https://img5.doubanio.com/view/ark_{#type}_cover/retina/public/{#id}.jpg'

# 源文件存储目录
DATA_DIRS = '%s/data' %(os.path.abspath('.'))

BOOK_COVER_DIRS = '%s/cover' %(DATA_DIRS)
# 初始化书籍封面目录
if not os.path.exists(BOOK_COVER_DIRS):
    os.makedirs(BOOK_COVER_DIRS)

# 输出文件存储目录
OUT_DATA_DIRS = '%s/out-data' %(os.path.abspath('.'))
if ENV == 'ONLINE':
    # 生产环境存储在/data目录
    OUT_DATA_DIRS = '/data/gk7-douban/mobi'

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
    'user': '',
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

'''
API接口全局状态
'''
API_STATUS = {
    'success': 'SUCCESS',
    'fail': 'FAIL',
    'abnormal': 'ABNORMAL'
}

API_URL = {
    'mail': 'http://gk7.pw:8001/mail'
}

## 书籍类型
BOOK_TYPE = {
    'gallery': 'gallery',
    'article': 'article',
    'column': 'column'
}

## 日志存储目录
LOG_DIRS = '%s/logs' %(os.path.abspath('.'))

## 图片默认最大宽度
PIC_MAX_WIDTH = 800

## 发送邮件类型[local, api]
SEND_MAIL_TYPE = 'local'
