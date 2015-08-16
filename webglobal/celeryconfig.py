#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
author by jacksyen[hyqiu.syen@gmail.com]
---------------------------------------
celery配置
"""
CELERY_ENABLE_UTC = True
CELERY_TIMEZONE = 'Europe/London'

BROKER_URL = 'amqp://gk7:gk7@localhost:5672/gk7-vhost'
CELERY_RESULT_BACKEND = 'amqp'

# 任务结果超时时间(秒)
CELERY_TASK_RESULT_EXPIRES = 24*60*60  # 24hours.

# email设置
ADMINS = (
    ('Jack Syen', 'hyqiu.syen@gmail.com'),
)

# 发送者邮箱设置
SERVER_MAIL = '418296229@qq.com'
EMAIL_HOST = 'smtp.qq.com'
EMAIL_PORT = 25
EMAIL_HOST_USER = '418296229'
EMAIL_HOST_PASSWORD = ''






