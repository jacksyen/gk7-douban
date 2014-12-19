#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
author by jacksyen[hyqiu.syen@gmail.com]
---------------------------------------
下载文件
"""
import urllib2
from webglobals.globals import GlobalThread
from multiprocessing.dummy import Pool as ThreadPool

class files:

    '''
    获取图片信息
    urls: 下载连接集合
    返回下载结果集合，可通过results[x].read()获取
    '''
    @staticmethod
    def get_images(urls):
        pool = ThreadPool(GlobalThread.POOL_NUMBER)
        results = pool.map(urllib2.urlopen, urls)
        pool.close()
        pool.join()
        for data in enumerate(results):
            pass
        return results
