#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
author by jacksyen[hyqiu.syen@gmail.com]
---------------------------------------
下载文件
"""
import os
import urllib2
import helper.aop as aop
from webglobal.globals import Global
from webglobal.globals import GlobalThread
from multiprocessing.dummy import Pool as ThreadPool

class Files:

    '''
    获取图片信息
    images_dir: 图片存储目录
    urls: 下载连接集合
    返回所有文件绝对路径集合
    '''
    @staticmethod
    @aop.exec_time
    def get_images(images_dir, urls):
        '''
        写入文件
        url: 图片下载连接
        返回文件绝对路径
        '''
        def write_file(url):
            data = urllib2.urlopen(url).read()
            # 文件路径
            file_path = '%s/%s' %(images_dir, url[url.rfind('/')+1:])
            with open(file_path, 'w') as f_data:
                f_data.write(data)
            return file_path

        # 判断目录是否存在
        if not os.path.exists(images_dir):
            os.makedirs(images_dir)

        # 多线程下载并存储图片
        pool = ThreadPool(GlobalThread.POOL_NUMBER)
        results = pool.map(write_file, urls)
        pool.close()
        pool.join()
        return results
