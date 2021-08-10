#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
author by jacksyen[hyqiu.syen@gmail.com]
---------------------------------------
发送邮件帮助类
"""
import smtplib

import globals

from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from util.log import logger
import util.aop as aop

class SendMail:

    def __init__(self):
        # 邮件服务
        self.server = smtplib.SMTP_SSL(globals.EMAIL_SMTP, globals.EMAIL_PORT, timeout=globals.EMAIL_TIMEOUT)
        #self.server.starttls()
        self.server.ehlo()
        self.server.login(globals.EMAIL_USER, globals.EMAIL_PWD)
        self.from_mail = globals.EMAIL_USER
        self.encode = globals.EMAIL_ENCODE

    @aop.exec_time
    def close(self):
        if self.server:
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
        msg['From'] = ("%s <" + self.from_mail +">") %(Header(author,'utf-8'),)
        msg['To'] = tomail
        msg['Subject'] = Header(title, self.encode)
        #msg["Accept-Language"]="zh-CN"
        #msg["Accept-Charset"]="ISO-8859-1,utf-8"
        att = MIMEText(open(file_path, 'rb').read(), 'base64', self.encode)
        att["Content-Type"] = 'application/octet-stream'
        att.add_header("Content-Disposition", "attachment", filename = file_name)
        msg.attach(att)
        # 发送邮件
        try:
            logger.info(u'开始发送邮件至%s...', tomail)
            self.server.sendmail(self.from_mail, tomail, msg.as_string())
            logger.info(u'发送邮件至%s完成', tomail)
        except Exception as err:
            logger.error(u'发送邮件至%s失败,%s', tomail, err)
            raise err
        finally:
            self.close()
