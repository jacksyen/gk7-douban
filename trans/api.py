# -*- coding: utf-8 -*-

import urllib
from helper.log import logger
import webglobal.globals as gk7
from helper.tasks import ApiTask, MailTask


class Api():

    @staticmethod
    def send_mail(email_id, attach_file, to_email, book_title, book_author):
        if gk7.SEND_MAIL_TYPE == 'api':
            data = {
                'email_id': email_id,
                'file_path': attach_file,
                'to_user': to_email,
                'title': book_title,
                'author': book_author
            }
            ApiTask.post.delay(gk7.API_URL.get('mail'), urllib.urlencode(data))
            logger.info(u'调用API发送邮件接口中...')
            return True
        # 其他类型
        # 发送邮件并修改待发送邮件状态
        MailTask.send.delay(email_id, attach_file, to_email, book_title, book_author)
        logger.info(u'发送邮件中...')
        return True
