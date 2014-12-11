#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
author by jacksyen[hyqiu.syen@gmail.com]
---------------------------------------
调用系统进程命令帮助
"""
from log import logger
from subprocess import call

class proc_helper:

    def __init__(self):
        pass

    '''
    转换文件[将html文件转换为epub格式]
    利用ebook-convert命令[基于calibre]
    input_file_path: 输入文件绝对路径
    out_file_dir: 输出文件目录绝对路径[如果不存在，则创建]
    '''
    @staticmethod
    def convert(input_file_path, out_file_dir):
        if not os.path.exists(out_file_dir):
            os.mkdir(out_file_dir)
        out_file_path = '%s.%s' %(input_file_path[0: input_file_path.split('/')[-1].rfind('.')], 'epub')
        code = call(['ebook-convert', input_file_path, out_file_path])
        if code != 0:
            logger.error(u'转换%s文件失败' %input_file_path)
            return None
        ## 转换成功
        return out_file_path
