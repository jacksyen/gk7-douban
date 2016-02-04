# -*- coding: utf-8 -*-

import web
import json

from helper.log import logger
from helper.dbase import MySQL
import helper.aop as aop
from db.tbl_wait_emails import Tbl_Wait_Emails

class History:
    
    def __init__(self):
        self.conn = MySQL.conn()
        self.db = self.conn.cursor()

    def __del__(self):
        if self.conn:
            MySQL.close(self.conn)

    def GET(self):
        return self.execute(web.input())

    def POST(self):
        return self.execute(web.input())    

    '''
    userId : 用户编码
    '''
    @aop.exec_api_time_consum
    def execute(self, args):
        try:
            user_id = args.get('userId')
            if not user_id:
                return json.dumps({'status': 'WRAN', 'msg': u'用户编码不能为空'})
            wait_emails = Tbl_Wait_Emails()
            emails = wait_emails.get_by_userId(user_id)
            if len(emails) == 0:
                return json.dumps({'status': 'SUCCESS', 'code': 'NONE', 'msg':u'没有推送的书籍'})
            return json.dumps({'status': 'SUCCESS', 'code': 'SUCCESS', 'data': emails, 'msg':u'没有推送的书籍'})
        except Exception, err:
            logger.error(u'推送异常,错误信息：%s，入参：%s' %(err, str(args)))
            return json.dumps({'status': 'ABNORMAL', 'msg': u'获取推送历史异常,%s，请联系:hyqiu.syen@gmail.com' %err})
