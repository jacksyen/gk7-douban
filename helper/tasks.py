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
import urllib2

from celery import Task
from celery import Celery

from log import logger
from helper.mail import SendMail
from webglobal import celeryconfig
from webglobal.globals import Global, Global_Status
from db.tbl_wait_emails import Tbl_Wait_Emails

app = Celery()
# 加载celery配置文件
app.config_from_object(celeryconfig)

class BaseTask(Task):

    abstract = True

    def after_return(self, *args, **kwargs):
        pass

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        logger.error(u'发送邮件失败，celery task id: %s, 参数:%s, 错误信息：%s' %(task_id, str(args), str(exc)))

    def on_retry(self, *args, **kwargs):
        pass

    def on_success(self, retval, task_id, args, kwargs):
        logger.info(u'发送邮件成功，参数:%s' %(task_id, str(args)))


'''
发送邮件任务
'''
class MailTask(object):
    
    '''
    发送邮件
    重试次数：5
    request_id: 请求ID
    attach_file: 附件文件路径
    to_email: 收件方
    title: 邮件标题
    auth: 邮件作者
    '''
    @app.task(base=BaseTask, max_retries=5)
    def send(request_id, attach_file, to_email, title, auth):
        try:
            mail = SendMail()
            wait_email = Tbl_Wait_Emails()

            # 发送邮件
            send_request = mail.send(attach_file, to_email, title, auth)
            # 更新发送邮件状态
            if send_request:
                wait_email.update_status(request_id, Global_Status.COMPLETE)
                return
            wait_email.update_status(request_id, Global_Status.ERROR)
        except Exception as err:
            ## 延迟30s后重试
            MailTask.send.retry(countdown=5, exc=err)

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
    @app.task(base=BaseTask, max_retries=5)
    def get_image(url, file_dir):
        try:
            data = urllib2.urlopen(url).read()
            # 文件路径
            file_path = '%s/%s' %(file_dir, url[url.rfind('/')+1:])
            with open(file_path, 'w') as f_data:
                f_data.write(data)
        except Exception as e:
            ## 延迟20s后重试
            DownloadTask.get_image.retry(countdown=20, exc=e)
        return file_path
