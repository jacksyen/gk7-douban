# -*- coding: utf-8 -*-

import smtplib

from email.header import Header
from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart

from dbase import SQLite
from webglobal.global import Global
from webglobal.global import Global_EMAILS_STATUS

from log import logger

class SendMail:

    def __init__(self):
        conn = SQLite.conn()
        db = conn.cursor()
        db.execute('SELECT * FROM %s' %Global.GLOBAL_DB_TBL_GLOBAL_NAME)
        global_info = db.fetchone()
        if global_info == None:
            logger.error(u'查询%s返回空' %Global.GLOBAL_DB_TBL_GLOBAL_NAME)
        self.server = smtplib.SMTP(global_info['smtp'], global_info['smtp_port'])
        self.server.starttls()
        self.server.login(global_info['email_user'], global_info['email_pwd'])
        self.from_mail = global_info['email_user']
        self.encode = global_info['email_encode']

    def close(self):
        if not self.server:
            self.server.quit()
            self.server.close()

    '''
    将信息添加至待发送邮件数据表
    filename: 附件名
    tomail: 发送到的email
    title: 标题
    author: 头部作者
    '''
    @staticmethod
    def add(filename, tomail, title, author):
        conn =  SQLite.conn()
        db = conn.cursor()
        db.execute('INSERT INTO %s(email_to_user, email_attach_file, email_title, email_auth, email_send_status, addtime, updatetime) VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s")' %(tomail, filename, title, auth, Global_EMAILS_STATUS.WAIT, DateUtil.getDate(format='%Y-%m-%d %H:%M:%S'), DateUtil.getDate(format='%Y-%m-%d %H:%M:%S')))
        if db.rowcount <= 0:
            logger.error(u'添加至邮件表错误，email: %s，标题：%s' %(tomail, title))
        conn.commit()

    def send(self, filename, tomail, title, author):
        # 构造附件
        msg = MIMEMultipart()
        msg['From'] = ("%s <" + self.from_mail +">") %(Header(author, self.encode),)
        msg['To'] = tomail
        msg['Subject'] = Header(title, self.encode)
        #msg["Accept-Language"]="zh-CN"
        #msg["Accept-Charset"]="ISO-8859-1,utf-8"
        att = MIMEText(open(filename, 'rb').read(), 'base64', self.encode)
        att["Content-Type"] = 'application/octet-stream'
        att.add_header("Content-Disposition", "attachment", filename = '%s' %filename.encode('gb2312'))
        msg.attach(att)
        # 发送邮件
        try:
            logger.info(u'开始发送邮件至%s...' %tomail)
            self.server.sendmail(msg['From'], tomail, msg.as_string())
            logger.info(u'发送邮件至%s完成' %tomail)
        except Exception, err:
            logger.error(u'发送邮件至%s失败,%s' %(tomail, err))
        finally:
            self.server.quit()
