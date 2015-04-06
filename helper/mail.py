#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
author by jacksyen[hyqiu.syen@gmail.com]
---------------------------------------
发送邮件帮助类
"""
import smtplib

from email.header import Header
from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart

from log import logger
import helper.aop as aop
import webglobal.globals as gk7

class SendMail:

    def __init__(self):
        # 邮件服务
        self.server = smtplib.SMTP(gk7.EMAIL.get('smtp'), gk7.EMAIL.get('port'), timeout=gk7.EMAIL.get('timeout'))
        self.server.starttls()
        self.server.login(gk7.EMAIL.get('user'), gk7.EMAIL.get('pwd'))
        self.from_mail = gk7.EMAIL.get('user')
        self.encode = gk7.EMAIL.get('encode')

    @aop.exec_time
    def close(self):
        if not self.server:
            self.server.quit()
            self.server.close()

    '''
    发送邮件,成功返回True，失败返回False
    filepath: 附件路径
    tomail: 对方邮件
    title: 标题
    author: 作者
    '''
    @aop.exec_time
    def send(self, file_path, tomail, title, author):
        file_name = file_path.split('/')[-1]
        # 构造附件
        msg = MIMEMultipart()
        msg['From'] = ("%s <" + self.from_mail +">") %(Header(author, self.encode),)
        msg['To'] = tomail
        msg['Subject'] = Header(title, self.encode)
        #msg["Accept-Language"]="zh-CN"
        #msg["Accept-Charset"]="ISO-8859-1,utf-8"
        att = MIMEText(open(file_path, 'rb').read(), 'base64', self.encode)
        att["Content-Type"] = 'application/octet-stream'
        att.add_header("Content-Disposition", "attachment", filename = file_name.encode('utf-8'))
        msg.attach(att)
        # 发送邮件
        try:
            logger.info(u'开始发送邮件至%s...', tomail)
            self.server.sendmail(msg['From'], tomail, msg.as_string())
            logger.info(u'发送邮件至%s完成', tomail)
        except Exception, err:
            logger.error(u'发送邮件至%s失败,%s', tomail, err)
            raise Exception, '发送邮件至%s失败,%s' %(tomail, err)
        finally:
            self.close()
