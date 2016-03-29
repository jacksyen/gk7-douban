# -*- coding: utf-8 -*-

import os
import sys
import time
import tools.markup as markup
import aop
from log import logger
import webglobal.globals as gk7

# 设置系统编码
reload(sys)
sys.setdefaultencoding('utf-8')

class HTML:

    '''
    初始化
    book_title: 图书标题
    #book_subtitle: 图书副标题
    file_dir: 源文件存储目录[绝对路径](格式：主目录/作者/书名标题/书籍大小)
    translator: 译者
    '''
    def __init__(self, book_title, book_author, file_dir):
        self.title = book_title
        #self.subtitle = book_subtitle
        self.author = book_author
        # 图片目录(格式：主目录/作者/书名标题)
        self.file_dir = file_dir
        # 创建HTML Page
        self.page = markup.page()
        # 初始化html
        self.page.init(lang='zh', title='%s' %self.title, charset='UTF-8', encoding='UTF-8', author=self.author)
        # 图片类型
        self.cxt_pic_type = ['medium', 'large', 'orig', 'small', 'tiny', 'smallshow']
        # 代码样式
        self.style_code = 'padding: 8px 0 8px 16px; color: #333; white-space: pre-wrap; background: #ebeae0; display: block; font-size: 12px; line-height: 16px;'
        self.style_code_inline = 'margin: 0 2px; padding: 3px 6px 0; -moz-border-radius: 3px; border-radius: 3px; color: #333; background-color: #e5e4db; font-size: 12px; word-break: normal; white-space: pre-wrap;'

        
    @aop.exec_out_time
    def create(self, send_type, book_posts):
        if send_type == gk7.BOOK_TYPE['gallery']:
            return self.create_gallery(book_posts)
        # 默认
        return self.create_article(book_posts)


    '''
    创建gallery类书籍
    book_pages: 书籍内容
    '''
    def create_gallery(self, book_pages):
        book_images_remote_path = []
        # 内容
        for page in book_pages:
            page_type = page.get('type')
            page_data = page.get('data')
            if page_type == 'illus':  ## 图片页
                # 获取图片信息
                illus_remote_src = self.get_illus(page_data)
                # 添加至所有图片远程路径集合
                book_images_remote_path.append(illus_remote_src)
            elif page_type == 'pagebreak': ## 分页符号
                pass
            elif page_type == 'container': ## 内容
                paragraphs = page_data.get('paragraphs')
                for paragraph in paragraphs:
                    paragraph_data = paragraph.get('data')
                    paragraph_data_text = paragraph_data.get('text')
                    text_content = ''
                    for text in paragraph_data_text:
                        if type(text) == unicode:
                            text_content += str(text)
                        else:
                            if text:
                                # dict
                                text_content += str(text.get('content'))
                    paragraph_data_format = paragraph_data.get('format')
                    self.page.p((text_content,), style=self.get_text_style(paragraph_data_format))
            else:
                logger.unknown(u'未知的内容type，data内容：%s' %(str(page_data)))
            ## 添加分割页面段落
            self.page.p(('',), class_=gk7.BOOK_PAGE_SPLIT)
        ## 片尾
        #self.page.p(('****本书由%s制作，如有问题，请发送邮件至 %s ****' %('jacksyen', 'hyqiu.syen@gmail.com'), ), style='font-size:13px; color:#333;')
        # 写入文件
        filename = self.write_html_to_file()
        return filename, book_images_remote_path

    '''
    创建html
    返回文件绝对路径
    data_contents: 书籍内容
    '''
    def create_article(self, book_posts):
        book_images_remote_path = []
        
        # 标题即是章节头标识
        title_class = 'bookTitle'
        if len(book_posts) > 1:
            title_class = 'chapter'
        for post in book_posts:
            # 文章主标题
            post_title = post.get('title')
            # 文章副标题
            post_subtitle = post.get('subtitle')
            # 文章作者
            post_author = [post.get('orig_author')]
            # 文章译者
            post_translator = post.get('translator')

            ## 标题
            self.page.h1((post_title,), class_=title_class)
            ## 副标题
            self.page.h2((post_subtitle,))
            ## 译者
            if post_translator:
                post_author.append(post_translator + u' 译')
            ## 作者
            self.page.p(tuple(post_author), style='text-align:left')

            ## 前言 or 导航
            #intr_item = (data_abstract,)
            #self.page.div(class_ = 'introduction')
            #self.page.p(intr_item, style='text-indent: 2em;')
            #self.page.div.close()
            
            ## 加载文章主体内容，返回文章所有图片远程路径
            book_images_remote_path.extend(self.get_post_content(post.get('contents')))
            ## 添加分割页面段落
            self.page.p(('',), class_=gk7.BOOK_PAGE_SPLIT)

        ## 片尾
        #self.page.p(('****本书由%s制作，如有问题，请发送邮件至 %s ****' %('jacksyen', 'hyqiu.syen@gmail.com'), ), style='font-size:13px; color:#333;')
        # 写入文件
        filename = self.write_html_to_file()

        return filename, book_images_remote_path

    '''
    获取文章主体内容
    contents：文章内容
    返回书籍所有图片远程路径集合
    '''
    def get_post_content(self, contents):
        ## 书籍所有图片远程路径集合
        book_images_remote_path = []
        for cxt in contents:
            cxt_type = cxt.get('type')
            # 具体内容
            cxt_data = cxt.get('data')
            if cxt_type == 'pagebreak': ## 分页符号
                self.page.p(('',), class_=gk7.BOOK_PAGE_SPLIT)
                continue
            if cxt_type == 'illus': ## 图片页
                # 获取图片信息
                illus_remote_src = self.get_illus(cxt_data)
                # 添加至所有图片远程路径集合
                book_images_remote_path.append(illus_remote_src)
                continue
            cxt_data_text = cxt_data.get('text')
            # 为空判断
            if cxt_data_text == '' or len(cxt_data_text) == 0:
                cxt_data_text = '&nbsp;'
            # 内容格式
            cxt_data_format = cxt_data.get('format')
            # 类型判断
            if cxt_type == 'headline': ## 标题头
                plaintexts = self.get_head_or_para_text(cxt_data_text)
                self.page.h2((plaintexts,), class_='chapter', style=self.get_text_style(cxt_data_format))
            elif cxt_type == 'paragraph': ## 段落
                # 获取段落内容
                plaintexts = self.get_head_or_para_text(cxt_data_text)
                # 添加段落至HTML
                self.page.p((plaintexts,), style=self.get_text_style(cxt_data_format, is_indent=True))
            elif cxt_type == 'code': ## 代码
                self.page.p(style=self.get_text_style(cxt_data_format))
                self.page.code((str(cxt_data_text).replace('<', '&lt;').replace('>', '&gt;'),), style=self.style_code)
                self.page.p.close()
            else:
                logger.unknown(u'未知的内容type，data内容：%s, 书籍名称:%s' %(str(cxt_data), self.title))
        return book_images_remote_path
    
    """
    获取headerline或者段落内容字符串，如存在注释，则包含
    cxt_data_text: 待解析的内容
    """
    def get_head_or_para_text(self, cxt_data_text):
        # 单条内容，直接返回
        if isinstance(cxt_data_text, list) == False:
            return str(cxt_data_text)
        # 多条内容，带注释
        plaintexts = []
        for text in cxt_data_text:
            kind = str(text.get('kind'))
            # 获取内容字符串
            content = self.get_head_or_para_text(text.get('content'))
            if kind == 'plaintext':
                plaintexts.append(content)
            elif kind == 'footnote':
                plaintexts.append('<font style="color:#333; font-size:13px;">[注：%s]</font>' %content)
            elif kind == 'emphasize':
                plaintexts.append('<font style="font-weight:bold;">%s</font>' %content)
            elif kind == 'code':
                plaintexts.append('<font style="%s">%s</font>' %(self.style_code_inline, content))
            elif kind == 'latex':
                plaintexts.append('<font style="color:red;">%s</font>' %(content))
            elif kind == 'strikethrough':
                plaintexts.append('<font style="text-decoration: line-through;">%s</font>' %content)
            elif kind == 'regular_script':
                plaintexts.append(content)
            else:
                plaintexts.append(content)
                logger.unknown(u'未知的data->text->kind，text内容：%s，图书标题：%s' %(str(cxt_data_text), self.title))
        return ''.join(plaintexts)

    '''
    获取图片段落
    cxt_data: 段落内容
    '''
    def get_illus(self, cxt_data):
        self.page.div()#class_='section'
        # 获取最大图片信息
        orig = cxt_data.get('size').get('orig')
        # 获取中等[medium]图片信息
        medium = self.get_cxt_pic(cxt_data)
        if medium == None:
            logger.error(u'获取图片信息失败')
        # 图片src
        medium_src = str(medium.get('src'))
        # 图片路径(格式：主目录/作者/书名标题/书籍大小/图片名称)
        cxt_image_path = '%s/%s' %(self.file_dir, medium_src[medium_src.rfind('/')+1:])
        self.page.img(width=orig.get('width'), height=orig.get('height'), src=cxt_image_path)
        # 添加图片备注
        legend = cxt_data.get('legend')
        legend_type = type(legend)
        if legend_type == unicode:
            self.page.label(str(legend), style='color:#555; font-size:.75em; line-height:1.5;')
        elif legend_type == dict:
            legend_data = legend.get('data')
            legend_data_paragraphs = legend_data.get('paragraphs') # []
            for legend_data_paragraph in legend_data_paragraphs:
                desc_text = self.get_legend_paragraph_text(legend_data_paragraph)
                self.page.label(desc_text, style='color:#555; font-size:.75em; line-height:1.5;')
        elif legend_type == list:
            for legend_data in legend:
                l_type = legend_data.get('type')
                l_data = legend_data.get('data')
                if l_type == 'paragraph':
                    desc_text = l_data.get('text')
                    desc_text_type = type(desc_text)
                    if desc_text_type == unicode:
                        self.page.label(str(desc_text), style='color:#555; font-size:.75em; line-height:1.5;')
                    elif desc_text_type == list:
                        for desc_text_data in desc_text:
                            self.page.label(str(desc_text_data.get('content')), style='font-weight:bold;font-size: .75em; color: #555;line-height: 1;font-style: normal;')
                    else:
                        logger.unknown(u'未知的内容:%s, 类型：%s' %(str(desc_text), str(desc_text_type)))
                else:
                    logger.unknown(u'未知的内容:%s, 类型：%s' %(str(l_data), str(l_type)))
        self.page.div.close()
        return medium_src
        

    '''
    获取图片备注
    多行，适合gallery类书籍
    legend_data_paragraph: 图例内容
    '''
    def get_legend_paragraph_text(self, legend_data_paragraph):
        img_desc_text = ''
        lp_type = legend_data_paragraph.get('type')
        lp_data = legend_data_paragraph.get('data')
        if lp_type == 'paragraph':
            for l_text in lp_data.get('text'):
                l_text_kind = l_text.get('kind')
                if l_text_kind == 'plaintext':
                    img_desc_text += str(l_text.get('content'))
        return img_desc_text
    
    
    '''
    获取<p>中的文字样式
    text_format: 豆瓣对应的文本格式
    is_indent: 是否缩进[True：添加text-indent:2em样式]
    '''
    def get_text_style(self, text_format, is_indent=False):
        text_base_style = 'line-height:2; min-height: 2em; text-align:%s; ' %(text_format.get('p_align'))
        if text_format.get('p_bold') == True:
            text_base_style += 'font-weight:bold;'
        if is_indent == True:
            text_base_style += 'text-indent: 2em;'
        return text_base_style

    '''
    获取图片信息
    cxt_data: 图片数据
    '''
    def get_cxt_pic(self, cxt_data, pic_type_num=0):
        pic_info = cxt_data.get('size').get(self.cxt_pic_type[pic_type_num])
        if pic_type_num == (len(self.cxt_pic_type) - 1):
            return None
        if not pic_info:
            pic_info = self.get_cxt_pic(cxt_data, pic_type_num=pic_type_num+1)
        return pic_info

    
    '''
    将html写入本地文件
    '''
    def write_html_to_file(self):
        # 写入文件
        if not os.path.exists(self.file_dir):
            os.makedirs(self.file_dir)
        filename = '%s/%d.html' %(self.file_dir, int(time.time()))
        output = open(filename, 'w')
        output.write(str(self.page))
        output.close()
        return filename
