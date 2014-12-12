# -*- coding:utf-8 -*-
import hashlib
import random
import time
import uuid

'''
MD5帮助类
'''
class MD5Util:

    @staticmethod
    def md5(param):
        md = hashlib.md5(param.encode('utf8'))
        return md.hexdigest()

'''
随机数帮助类
'''
class RandomUtil:

    @staticmethod
    def random6Str():
        num = random.randint(100000, 999999)
        return num

    @staticmethod
    def random9Str():
        num = random.random() * (1<<29)
        return int(num)

    @staticmethod
    def random16Str():
        num = random.randint(10,99)
        result = '%.4f%d' %(time.time(), num)
        result = result.replace('.','')
        return result

    @staticmethod
    def random32Str():
        return uuid.uuid1().hex


'''
日期帮助类
'''
class DateUtil:

    @staticmethod
    def getDate(format='%Y%m'):
        t = time.localtime(time.time())
        return time.strftime(format, t)

'''
class JSONUtil:

    @staticmethod
    def toJson(json_str):
        try:
            return json.loads(json_str)
        except e:
            return None

'''
