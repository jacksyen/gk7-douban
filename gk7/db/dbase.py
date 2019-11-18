#-*- coding:utf-8 -*-

'''
数据库连接池
'''

import pymysql
import globals
import util.aop as aop
from util.log import logger
from util.util import DateUtil

class Database:

    def __init__(self):
        try:
            self._conn =  pymysql.connect(host=globals.DB_HOST, port=globals.DB_PORT, user=globals.DB_USER, passwd=globals.DB_PASSWD, db=globals.DB_NAME, charset='UTF8', cursorclass=pymysql.cursors.DictCursor)
            self.__cursor = self._conn.cursor()
            logger.info(u'数据库连接成功')
        except Exception as err:
            logger.error(u'连接数据库异常,%s', err)

    def close(self):
        """关闭游标和数据库连接"""
        if self.__cursor is not None:
            self.__cursor.close()
        self._conn.close()

    def __getCursor(self):
        """获取游标"""
        if self.__cursor is None:
            self.__cursor = self._conn.cursor()
        return self.__cursor

    '''
    添加书籍图片路径信息
    ebook_id: 书籍ID
    book_images_remote_path: (书籍图片远程路径)
    '''
    @aop.exec_time
    def book_img_add(self, images_id, book_id, book_images_remote_path):
        self.__getCursor().execute('''INSERT INTO gk7_douban_book_img(images_id, book_id, book_images_remote_path, addtime) VALUES (%s, %s, %s, %s)''', (images_id, book_id, globals.BOOK_IMG_PATH_SPLIT.join(book_images_remote_path), DateUtil.getDate(format='%Y-%m-%d %H:%M:%S')))
        self._conn.commit()

    '''
    根据书籍ID获取图书的图片信息
    book_id: 书籍ID
    '''
    @aop.exec_time
    def book_img_get(self, book_id):
        self.__getCursor().execute('''SELECT book_images_remote_path, addtime, updatetime FROM gk7_douban_book_img WHERE book_id = %s''', (book_id, ))
        return self.__getCursor().fetchone()

    '''
    根据书籍ID更新书籍本地图片
    book_id: 书籍ID
    book_images_local_path: 书籍本地图片集合
    '''
    @aop.exec_time
    def book_img_update_local_path(self, book_id, book_images_local_path):
        self.__getCursor().execute('''UPDATE gk7_douban_book_img SET book_images_local_path = %s, updatetime = %s WHERE book_id = %s''', (globals.BOOK_IMG_PATH_SPLIT.join(book_images_local_path), DateUtil.getDate(format='%Y-%m-%d %H:%M:%S'), book_id))
        self._conn.commit()


    '''
    添加书籍信息
    返回书籍ID，即book_id
    
    book_number: 书籍号码(格式：作者ID_书名标题)
    book_title: 标题
    book_subtitle: 副标题
    book_author: 作者
    book_size: 书籍大小(客户端传递的bookData大小，即豆瓣文章加密字符串大小)
    '''
    @aop.exec_time
    def book_add(self, book_id, ebook_id, book_title, book_subtitle, book_author, book_size, book_cover_remote_path):
        self.__getCursor().execute('''INSERT INTO gk7_douban_books(id, ebook_id, book_title, book_subtitle, book_author, book_size, book_cover_remote_path, addtime) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)''', (book_id, ebook_id, book_title, book_subtitle, book_author, book_size, book_cover_remote_path, DateUtil.getDate(format='%Y-%m-%d %H:%M:%S')))
        self._conn.commit()

    @aop.exec_time
    def book_delete(self, book_id):
        self.__getCursor().execute('''DELETE FROM gk7_douban_books WHERE id = %s''', (book_id,))
        self._conn.commit()

    '''
    根据书籍号码和书籍大小查询书籍信息
    ebook_id: 书籍号码(对应douban书籍ID)
    book_size: 书籍大小(客户端传递的bookData大小，即豆瓣文章加密字符串大小)
    '''
    @aop.exec_time
    def book_get(self, ebook_id, book_size):
        self.__getCursor().execute('''SELECT id, ebook_id, book_title, book_subtitle, book_author, book_file_path, addtime, updatetime FROM gk7_douban_books WHERE ebook_id =%s AND book_size = %s AND book_file_path !=""''', (ebook_id, book_size))
        rows = self.__getCursor().fetchone()
        # result = [dict(zip(self.__getCursor().description, row)) for row in rows]
        print(rows)
        return rows

    '''
    根据书籍ID查询书籍信息
    book_id: 书籍ID
    '''
    @aop.exec_time
    def book_get_by_book_id(self, book_id):
        self.__getCursor().execute('''SELECT id, ebook_id, book_title, book_subtitle, book_author, book_file_path, book_size, book_cover_local_path FROM gk7_douban_books WHERE id =%s''', (book_id, ))
        return self.__getCursor().fetchone()

    '''
    根据书籍号码修改书籍文件路径
    book_id: 书籍ID
    book_file_path: 书籍文件路径(绝对路径)
    '''
    @aop.exec_time
    def book_update_file_path(self, book_id, book_file_path):
        self.__getCursor().execute('''UPDATE gk7_douban_books SET book_file_path = %s WHERE id = %s''', (book_file_path, book_id))
        self._conn.commit()

    '''
    更新书籍封面
    book_id: 书籍ID
    book_cover_path: 书籍封面路径
    '''
    @aop.exec_time
    def book_update_cover(self, book_id, book_cover_local_path):
        self.__getCursor().execute('''UPDATE gk7_douban_books SET book_cover_local_path = %s WHERE id = %s''', (book_cover_local_path, book_id))
        self._conn.commit()


    '''
    增加转换信息
    convert_id: 转换id
    request_user: 请求用户
    book_html_local_path: 书籍html本地路径
    '''
    @aop.exec_time
    def convert_add(self, convert_id, request_user, book_html_local_path):
        self.__getCursor().execute('''INSERT INTO gk7_douban_wait_converts(convert_id, request_user, book_html_local_path, convert_status, addtime) VALUES(%s, %s, %s, %s, %s)''', (convert_id, request_user, book_html_local_path, globals.STATUS.get('wait'), DateUtil.getDate(format='%Y-%m-%d %H:%M:%S')))
        self._conn.commit()

    '''
    根据转换ID获取待转换书籍信息
    convert_id: 转换ID
    '''
    @aop.exec_time
    def convert_get(self, convert_id):
        self.__getCursor().execute('''SELECT convert_id, book_html_local_path, book_convert_file_path FROM gk7_douban_wait_converts WHERE convert_id = %s''', (convert_id, ))
        return self.__getCursor().fetchone()

    '''
    根据请求ID更新书籍转换状态,添加书籍转换完成的绝对路径
    status: 转换状态
    convert_id: 请求ID
    '''
    @aop.exec_time
    def convert_update_status(self, status, convert_id, book_convert_path=None):
        self.__getCursor().execute('''UPDATE gk7_douban_wait_converts SET convert_status = %s, book_convert_file_path = %s WHERE convert_id =%s''', (status, book_convert_path, convert_id))
        self._conn.commit()

    '''
    将信息添加至待发送邮件数据表
    email_id: 待发送邮件Id
    tomail: 发送到的email
    title: 标题
    author: 作者
    '''
    @aop.exec_time
    def email_add(self, email_id, tomail, title, auth):
        self.__getCursor().execute('''INSERT INTO gk7_douban_wait_emails(email_id, email_to_user, email_title, email_auth, email_send_status, addtime) VALUES (%s, %s, %s, %s, %s, %s)''', (email_id, tomail, title, auth, globals.STATUS.get('wait'), DateUtil.getDate(format='%Y-%m-%d %H:%M:%S')))
        self._conn.commit()

    '''
    将信息添加至待发送邮件数据表
    email_id: 待发送邮件Id
    tomail: 发送到的email
    title: 标题
    author: 作者
    attach_file: 附件
    '''
    @aop.exec_time
    def email_add_full(self, email_id, tomail, title, auth, attach_file):
        self.__getCursor().execute('''INSERT INTO gk7_douban_wait_emails(email_id, email_to_user, email_attach_file, email_title, email_auth, email_send_status, addtime) VALUES (%s, %s, %s, %s, %s, %s, %s)''', (email_id, tomail, attach_file, title, auth, globals.STATUS.get('wait'), DateUtil.getDate(format='%Y-%m-%d %H:%M:%S')))
        self._conn.commit()


    '''
    根据请求ID获取待发送邮件信息
    request_id: 请求ID
    '''
    @aop.exec_time
    def email_get(self, email_id):
        self.__getCursor().execute('''SELECT email_id, email_to_user, email_attach_file, email_title, email_auth, email_send_status FROM gk7_douban_wait_emails WHERE email_id =%s''', (email_id, ))
        return self.__getCursor().fetchone()

    '''
    根据请求ID修改发送邮件状态
    email_id: 邮件ID
    send_status: 发送状态
    '''
    @aop.exec_time
    def email_update_status(self, email_id, send_status):
        self.__getCursor().execute('''UPDATE gk7_douban_wait_emails SET email_send_status = %s WHERE email_id = %s''', (send_status, email_id))
        self._conn.commit()

    '''
    根据邮件ID修改待发送邮件附件信息
    email_id: 邮件ID
    attach_file: 附件
    '''
    @aop.exec_time
    def email_update_attach_file(self, email_id, attach_file):
        self.__getCursor().execute('''UPDATE gk7_douban_wait_emails SET email_attach_file = %s WHERE email_id = %s''', (attach_file, email_id))
        self._conn.commit()
