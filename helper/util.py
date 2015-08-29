# -*- coding:utf-8 -*-
import hashlib
import random
import time
import uuid
import Image

'''
图片帮助类
'''
class ImageUtil:
    
    '''
    压缩图片
    file_path: 文件路径
    new_width: 新宽度，如果原图片小于新宽度，则只压缩，不缩放
    '''
    @staticmethod
    def compress(file_path, new_width):
        im = Image.open(file_path)
        width,height = im.size
        if width < new_width:
            new_width = width
        ratio = 1.0 * height / width
        new_height = int(new_width * ratio)
        new_size = (new_width, new_height)
        #插值缩放图像
        out = im.resize(new_size, Image.ANTIALIAS)
        # 保存并替换原图片
        out.convert('RGB').save(file_path)


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
