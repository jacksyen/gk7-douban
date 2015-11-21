#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
author by jacksyen[hyqiu.syen@gmail.com]
---------------------------------------
调用系统进程命令帮助
"""
import os

from log import logger
from subprocess import call
import helper.aop as aop
import webglobal.globals as gk7

class proc_helper:

    def __init__(self):
        pass

    '''
    转换文件[将html文件转换为epub格式]
    利用ebook-convert命令[基于calibre]
    input_file_path: 输入文件绝对路径
    out_file_dir: 输出文件目录绝对路径[如果不存在，则创建]
    author: 作者
    cover: 封面
    '''
    @staticmethod
    @aop.exec_time
    def convert(input_file_path, out_file_dir, author, cover):
        if not os.path.exists(out_file_dir):
            os.makedirs(out_file_dir)
        # 文件名
        file_name = input_file_path.split('/')[-1]
        # 输出文件绝对路径
        out_file_path = '%s/%s.%s' %(out_file_dir, file_name[0: file_name.rfind('.')], gk7.OUT_FILE_FORMAT)
        ## 
        ## 说明：
        ## 调用系统命令：ebook-convert input_file out_file --authors <author> --cover <img> --language zh --chapter-mark "none" --page-breaks-before '//*[@class="pagebreak"]'
        ## --cover 书籍封面
        ## --chapter-mark 设置标注章节的模式，none：不会在章节前插入控制
        ## --page-breaks-before: XPath表达式，在指定元素前插入分页符
        ## 
        params = ['ebook-convert']
        params.append(input_file_path)
        params.append(out_file_path)
        if author:
            params.append('--authors')
            params.append(author)
        if cover:
            params.append('--cover')
            params.append(cover)
        params.append('--language')
        params.append('zh')
        params.append('--input-encoding')
        params.append('UTF-8')
        params.append('--chapter-mark')
        params.append('none')
        params.append('--page-breaks-before')
        params.append('//*[@class="%s"]' %gk7.BOOK_PAGE_SPLIT)
        ## 调用
        call(params)
        #call(['ebook-convert', input_file_path, out_file_path, '--authors', author, '--cover', cover, '--chapter-mark', 'none', '--page-breaks-before', '//*[@class="%s"]' %gk7.BOOK_PAGE_SPLIT])
        ## 转换成功
        return out_file_path
