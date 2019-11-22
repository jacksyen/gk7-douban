# -*- coding: utf-8 -*-

import urllib
import globals
from util.log import logger
from task.tasks import ApiTask, MailTask


class Api():

    @staticmethod
    def send_mail(email_id, attach_file, to_email, book_title, book_author):
        # 其他类型
        # 发送邮件并修改待发送邮件状态
        MailTask.send.delay(email_id, attach_file, to_email, book_title, book_author)
        logger.info(u'发送邮件中...')
        return True
