# -*- coding: utf-8 -*-

import os
import sys
import tools.markup as markup

# 设置系统编码
reload(sys)
sys.setdefaultencoding('utf-8')

class HTML:

    def __init__(self, book_title, book_subtitle, book_author):
        self.title = book_title
        self.subtitle = book_subtitle
        self.author = book_author
        # 创建HTML Page
        self.page = markup.page()
        # 初始化html
        self.page.init(title='%s' %self.title, charset='UTF-8', author=self.author)


    '''
    创建html
    返回文件绝对路径
    '''
    def create(self, data_json, data_contents):
        ## 标题
        self.page.h1((self.title,), class_='bookTitle')
        self.page.h2((self.subtitle,))
        ## 作者
        self.page.p((self.author,), style='text-align:right')

        ## 前言 or 导航
        intr_item = (str(data_json.get('abstract')),)
        self.page.div(class_ = 'introduction')
        self.page.p(intr_item, style='text-indent: 2em;')
        self.page.div.close()

        ## 内容
        for cxt in data_contents:
            cxt_type = cxt.get('type')
            if cxt_type == 'pagebreak':
                continue
            # 具体内容
            cxt_data_text = cxt.get('data').get('text')
            if cxt_type == 'headline':
                self.page.h2((str(cxt_data_text),), class_='chapter')
            elif cxt_type == 'paragraph':
                # 多条内容，带注释
                if isinstance(cxt_data_text, list):
                    plaintexts, footnotes = self.get_data_text_list(cxt_data_text)
                    self.page.p((plaintexts,), style='text-indent: 2em;')
                    if len(footnotes) > 0:
                        self.page.p(tuple(footnotes), style='color:#333;font-size:13px;')
                else:
                    chapter_item = (str(cxt_data_text),)
                    self.page.p(chapter_item, style='text-indent: 2em;')

        ## 片尾
        self.page.p(('****本书由%s制作，如有问题，请发送邮件至 %s ****' %('jacksyen', 'hyqiu.syen@gmail.com'), ), style='font-size:13px; color:#333;')

        # 写入文件
        path = 'data'
        if not os.path.exists(path):
            os.mkdir(path)
        filename = '%s/%s.html' %(os.path.abspath(path), self.title)
        output = open(filename, 'w')
        output.write(str(self.page))
        output.close()
        return filename


    '''
    获取内容集合，包含注释
    '''
    def get_data_text_list(self, cxt_data_text):
        plaintexts = ''
        footnotes = []
        index = 1
        desc = ''
        for text_index, text in enumerate(cxt_data_text):
            kind = str(text.get('kind'))
            content = str(text.get('content'))
            if kind == 'plaintext':
                plaintexts = plaintexts + content
                if text_index < (len(cxt_data_text) -1):
                    desc = '[%d]' %index
                    plaintexts = plaintexts + desc
                    index = index + 1
            elif kind == 'footnote':
                footnotes.append(desc + content)
        return plaintexts, footnotes    
