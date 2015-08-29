# -*- coding: utf-8 -*-
import json

from helper.log import logger
import webglobal.globals as gk7

class Common():

    @staticmethod
    def send_mail(self, send_mail_type, email_id, attach_file, to_email, book_title, book_author):
        if send_mail_type == 'gmail':
            import urllib, urllib2
            data = {
                'email_id': email_id,
                'file_path': attach_file,
                'to_user': to_email,
                'title': book_title,
                'author': book_author
            }
            result = urllib2.urlopen(gk7.API_URL.get('mail'), urllib.urlencode(data)).read()
            if not result:
                logger.error(u'发送邮件结果为空')
                return false
            json_result = json.loads(result)
            if str(json_result.get('status')) != gk7.API_STATUS.get('success'):
                logger.error(u'发送邮件失败,API接口返回：%s' % str(result))
                return false
            return true
        # 其他类型
        # 发送邮件并修改待发送邮件状态
        from helper.tasks import MailTask
        MailTask.send.delay(email_id, attach_file, to_email, book_title, book_author)
        return true
