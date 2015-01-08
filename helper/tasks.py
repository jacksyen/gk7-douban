#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
author by jacksyen[hyqiu.syen@gmail.com]
---------------------------------------
decorator
"""
import urllib2
from celery import Task
from celery import Celery
from webglobal import celeryconfig

app = Celery()
# 加载celery配置文件
app.config_from_object(celeryconfig)

'''
下载任务队列
'''
class DownloadTask(object):

    '''
    调用：DownloadTask.get_image.delay(<url>, <file_dir>)
    url: 下载URL
    file_dir: 文件本地存储目录
    '''
    @app.task(name='', base=BaseTask)
    def get_image(url, file_dir):
        try:
            data = urllib2.urlopen(url).read()
            # 文件路径
            file_path = '%s/%s' %(file_dir, url[url.rfind('/')+1:])
            with open(file_path, 'w') as f_data:
                f_data.write(data)
        except Exception as e:
            print u'错误'
            ## 延迟20s后重试
            DownloadTask.get_image.retry(countdown=20, exc=e)
        return file_path



class BaseTask(Task):

    abstract = True

    def after_return(self, *args, **kwargs):
        pass

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        pass

    def on_retry(self, exc, task_id, args, kwargs, einfo):
        pass

    def on_success(self, retval, task_id, args, kwargs):
        pass
