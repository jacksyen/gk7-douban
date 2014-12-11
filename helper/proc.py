#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
author by jacksyen[hyqiu.syen@gmail.com]
---------------------------------------
调用系统进程命令帮助
"""
from subprocess import call

class ProcessHelper:

    def __init__(self):
        pass

    '''
    转换文件[将html文件转换为epub格式]
    利用ebook-convert命令[基于calibre]
    input_file_path: 输入文件绝对路径
    out_file_dir: 输出文件目录绝对路径
    '''
    def convert(self, input_file_path, out_file_dir):
        out_file_path = '%s.%s' %(input_file_path[0: input_file_path.split('/')[-1].rfind('.')], 'epub')
        code = call(['ebook-convert', input_file_path, out_file_path])
        if code != 0:
            pass
        ## 转换成功
        return out_file_path
