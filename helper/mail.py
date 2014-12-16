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
from dbase import SQLite
import helper.aop as aop
from db.tbl_globals import Tbl_Global
from webglobal.globals import Global, Global_Status

class SendMail:

    def __init__(self):
        # 获取全局邮件配置信息
        global_info = Tbl_Global()
        global_email_info = global_info.get_global_email()
        if global_email_info == None:
            logger.error(u'查询%s返回空', Global.GLOBAL_DB_TBL_GLOBAL_NAME)
            # TODO
        # 邮件服务
        self.server = smtplib.SMTP(str(global_email_info['smtp']), str(global_email_info['smtp_port']))
        self.server.starttls()
        self.server.login(str(global_email_info['email_user']), str(global_email_info['email_pwd']))
        self.from_mail = str(global_email_info['email_user'])
        self.encode = str(global_email_info['email_encode'])

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
        att.add_header("Content-Disposition", "attachment", filename = '%s' %(file_name.encode('gb2312')))
        msg.attach(att)
        # 发送邮件
        try:
            logger.info(u'开始发送邮件至%s...', tomail)
            self.server.sendmail(msg['From'], tomail, msg.as_string())
            logger.info(u'发送邮件至%s完成', tomail)
            return True
        except Exception, err:
            logger.error(u'发送邮件至%s失败,%s', tomail, err)
            return False
        finally:
            self.server.quit()
