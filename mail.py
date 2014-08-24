# -*- coding: utf-8 -*-

import smtplib

from email.header import Header
from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart

from log import logger

class SendMail:

    def __init__(self):
        self.server = smtplib.SMTP('smtp.qq.com', '587')
        self.server.starttls()
        self.server.login('461166828@qq.com', 'Syen19890828')
        self.from_mail = '461166828@qq.com'

    def close(self):
        if not self.server:
            self.server.quit()
            self.server.close()

    def send(self, filename, tomail, title, author):
        # 构造附件
        msg = MIMEMultipart()
        msg['From'] = ("%s <" + self.from_mail +">") %(Header(author,'utf-8'),)
        msg['To'] = tomail
        msg['Subject'] = Header(title, 'utf-8')
        #msg["Accept-Language"]="zh-CN"
        #msg["Accept-Charset"]="ISO-8859-1,utf-8"
        att = MIMEText(open(filename, 'rb').read(), 'base64', 'utf-8')
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
