# -*- coding: utf-8 -*-

import os
import sys
import tools.markup as markup
import aop
from webglobal.globals import Global

# 设置系统编码
reload(sys)
sys.setdefaultencoding('utf-8')

class HTML:
    
    '''
    '%s/%s/%s' %(Global.GLOBAL_DATA_DIRS, self.author, self.title)
    '''
    def __init__(self, book_title, book_subtitle, book_author, images_dir, translator):
        self.title = book_title
        self.subtitle = book_subtitle
        self.author = book_author
        self.translator = translator
        # 图片目录(格式：主目录/作者/书名标题)
        self.images_dir = images_dir
        # 创建HTML Page
        self.page = markup.page()
        # 初始化html
        self.page.init(title='%s' %self.title, charset='UTF-8', author=self.author)


    '''
    创建html
    返回文件绝对路径
    data_contents: 书籍内容
    '''
    @aop.exec_out_time
    def create(self, data_contents):
        ## 标题
        self.page.h1((self.title,), class_='bookTitle')
        self.page.h2((self.subtitle,))
        book_author = [self.author]
        if self.translator:
            book_author.append(self.translator.join(u' 译'))
        ## 作者
        self.page.p(tuple(book_author), style='text-align:left')

        ## 前言 or 导航
        #intr_item = (data_abstract,)
        #self.page.div(class_ = 'introduction')
        #self.page.p(intr_item, style='text-indent: 2em;')
        #self.page.div.close()

        ## 书籍所有图片远程路径集合
        book_images_remote_path = []

        ## 内容
        for cxt in data_contents:
            cxt_type = cxt.get('type')
            # 具体内容
            cxt_data = cxt.get('data')
            if cxt_type == 'pagebreak': ## 分页符号
                self.page.p(('',), class_=Global.GLOBAL_BOOK_PAGE_SPLIT)
                continue
            if cxt_type == 'illus': ## 图片页
                self.page.div()#class_='section'
                # 获取最大图片信息
                orig = cxt_data.get('size').get('orig')
                # 获取中等[medium]图片信息
                medium = cxt_data.get('size').get('medium')
                # 图片src
                medium_src = str(medium.get('src'))
                # 图片路径(格式：主目录/作者/书名标题/图片名称)
                cxt_image_path = '%s/%s' %(self.images_dir, medium_src[medium_src.rfind('/')+1:])
                self.page.img(width=orig.get('width'), height=orig.get('height'), src=cxt_image_path)
                # 添加图片备注
                legend = str(cxt_data.get('legend'))
                if legend:
                    self.page.label(legend, style='color:#555; font-size:.75em; line-height:1.5;')
                self.page.div.close()
                # 添加至所有图片远程路径集合
                book_images_remote_path.append(medium_src)
                continue
            cxt_data_text = cxt_data.get('text')
            # 为空判断
            if cxt_data_text == '' or len(cxt_data_text) == 0:
                cxt_data_text = '&nbsp'
            if cxt_type == 'headline':
                self.page.h2((str(cxt_data_text),), class_='chapter', style='text-align:center; line-height:2; font-size:13px; min-height: 2em;')
            elif cxt_type == 'paragraph':
                text_format = cxt_data.get('format')
                # 多条内容，带注释
                if isinstance(cxt_data_text, list):
                    plaintexts, footnotes = self.get_data_text_list(cxt_data_text)
                    self.page.p((plaintexts,), style=self.get_text_style(text_format))
                    if len(footnotes) > 0:
                        self.page.p(tuple(footnotes), style='color:#333;font-size:13px;')
                else:
                    
                    chapter_item = (str(cxt_data_text),)
                    self.page.p(chapter_item, style=self.get_text_style(text_format))

        ## 片尾
        self.page.p(('****本书由%s制作，如有问题，请发送邮件至 %s ****' %('jacksyen', 'hyqiu.syen@gmail.com'), ), style='font-size:13px; color:#333;')

        # 写入文件
        if not os.path.exists(Global.GLOBAL_DATA_DIRS):
            os.mkdir(Global.GLOBAL_DATA_DIRS)
        filename = '%s/%s.html' %(os.path.abspath(Global.GLOBAL_DATA_DIRS), self.title)
        output = open(filename, 'w')
        output.write(str(self.page))
        output.close()
        return filename, book_images_remote_path

    
    '''
    获取<p>中的文字样式
    text_format: 豆瓣对应的文本格式
    '''
    def get_text_style(self, text_format):
        text_base_style = 'text-indent: 2em; line-height:2; min-height: 2em; text-align:%s' %(text_format.get('p_align'))
        if text_format.get('p_bold') == 'true':
            text_base_style = text_base_style.join('font-weight:bold;')
        return text_base_style

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
