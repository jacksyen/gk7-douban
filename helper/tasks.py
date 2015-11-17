#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
author by jacksyen[hyqiu.syen@gmail.com]
---------------------------------------
celery异步任务
server: 
    #[root用户运行]
    export C_FORCE_ROOT='true'
    celery -A helper.tasks worker -l info
"""
import os
import json
import urllib2

from celery import Task
from celery import Celery

from log import logger
from util import ImageUtil
from helper.mail import SendMail
from webglobal import celeryconfig
from db.tbl_wait_emails import Tbl_Wait_Emails
import webglobal.globals as gk7

app = Celery()
# 加载celery配置文件
app.config_from_object(celeryconfig)

class BaseTask(Task):

    abstract = True

    def after_return(self, *args, **kwargs):
        pass

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        try:
            logger.error(u'发送邮件失败，celery task id: %s, 参数:%s, 错误信息：%s' %(task_id, str(args), str(exc)))
            wait_email = Tbl_Wait_Emails()
            wait_email.update_status(str(args[0]), gk7.STATUS.get('error'))
        except Exception as e:
            logger.error(u'更新发送邮件状态异常，错误:%s,参数:%s' %(str(e), str(args)))

    def on_retry(self, *args, **kwargs):
        pass

    def on_success(self, retval, task_id, args, kwargs):
        try:
            logger.info(u'发送邮件成功，参数:%s' %str(args))
            # 更新发送邮件状态
            wait_email = Tbl_Wait_Emails()
            wait_email.update_status(str(args[0]), gk7.STATUS.get('complete'))
        except Exception as e:
            logger.error(u'更新发送邮件状态异常，错误:%s,参数:%s' %(str(e), str(args)))

'''
API base task
'''
class ApiBaseTask(Task):

    abstract = True

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        logger.error(u'调用API接口失败，celery task id:%s, 参数:%s, 错误信息:%s' %(task_id, str(args), str(exc)))

'''
Download base task
'''
class DownloadBaseTask(Task):

    abstract = True

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        logger.error(u'下载文件失败，celery task id:%s，参数:%s，错误信息：%s' %(task_id, str(args), str(exc)))

'''
调用API接口
'''
class ApiTask(object):
    
    @app.task(base=ApiBaseTask, max_retries=5)
    def post(url, params):
        try:
            result = urllib2.urlopen(url, params, timeout=gk7.HTTP_TIME_OUT).read()
            if not result:
                ApiTask.post.retry(countdown=20, exc=e)
                return
            json_result = json.loads(result)
            if str(json_result.get('status')) != gk7.API_STATUS.get('success'):
                ApiTask.post.retry(countdown=20, exc=e)
                return
        except Exception as e:
            # 延迟20s重试
            ApiTask.post.retry(countdown=20, exc=e)
        return json_result


'''
发送邮件任务
'''
class MailTask(object):
    
    '''
    发送邮件,发送失败后间隔30秒重新发送
    重试次数：5
    mail_id: 邮件ID
    attach_file: 附件文件路径
    to_email: 收件方
    title: 邮件标题
    auth: 邮件作者
    '''
    @app.task(base=BaseTask, max_retries=5)
    def send(mail_id, attach_file, to_email, title, auth):
        try:
            mail = SendMail()
            # 发送邮件
            mail.send(attach_file, to_email, title, auth)
        except Exception as err:
            ## 延迟30s后重试
            MailTask.send.retry(countdown=30, exc=err)

'''
下载任务队列
'''
class DownloadTask(object):

    '''
    调用：DownloadTask.get_image.delay(<url>, <file_dir>)
    最大重试次数：5
    url: 下载URL
    file_dir: 文件本地存储目录
    '''
    @app.task(base=DownloadBaseTask, max_retries=5)
    def get_image(url, file_dir):
        try:
            data = urllib2.urlopen(url, timeout=gk7.HTTP_TIME_OUT).read()
            # 文件路径
            file_path = '%s/%s' %(file_dir, url[url.rfind('/')+1:])
            with open(file_path, 'w') as f_data:
                f_data.write(data)
            # 压缩
            ImageUtil.compress(file_path, gk7.PIC_MAX_WIDTH)
        except Exception as e:
            ## 延迟20s后重试
            DownloadTask.get_image.retry(countdown=20, exc=e)
        return file_path
