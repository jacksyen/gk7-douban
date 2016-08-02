#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
author by jacksyen[hyqiu.syen@gmail.com]
https://img1.doubanio.com/dae/staticng/s/ark/latest/js/dist/reader/4.b5cafd1dd8d845646b6d.js

---------------------------------------
解密豆瓣阅读文章
"""
import re
import aop

class decrypt:

    '''
    解密字符串
    decrypt_str: 加密后的字符串
    '''
    @staticmethod
    @aop.exec_time_consum
    def parse(decrypt_str):
        def xtoy(a):
            i = 0
            ll = []
            while i<len(a):
                c = a[i]
                i = i + 1
                if i < len(a):
                    ll.append(256* c + a[i])
                i = i + 1
            return ''.join(map(unichr, ll))

        _hex_chs = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz$_~'

        _key = [37, 20, 41, 59, 53, 8, 24, 5, 62, 31, 4, 32, 6, 50, 36, 63, 47, 42, 30, 39, 12, 3, 9, 45, 29, 23, 56, 2, 16, 61, 52, 44, 25, 35, 51, 0, 13, 43, 46, 40, 15, 27, 17, 57, 28, 54, 1, 60, 21, 22, 14, 49, 34, 33, 10, 58, 55, 19, 26, 11, 18, 48, 38, 7]

        _str_reg = re.compile(r'[^0-9A-Za-z$_~]')
        # 初始化
        key = []
        tbl = {}
        i = 0
        for i in range(64):
            key.append(_hex_chs[_key[i]])
            tbl[key[i]] = i
        pad = _hex_chs[64]

        n1 = n2 = n3 = n4 = sa = []
        i = c = 0
        # 替换字符串
        decrypt_str = _str_reg.sub('', decrypt_str)
        while i<len(decrypt_str):
            n1 = n2 = n3 = n4 = 0
            if tbl.has_key(decrypt_str[i]):
                n1 = tbl[decrypt_str[i]]
            i = i + 1
            if i <len(decrypt_str):
                if tbl.has_key(decrypt_str[i]):
                    n2 = tbl[decrypt_str[i]]
            i = i + 1
            if i <len(decrypt_str):
                if tbl.has_key(decrypt_str[i]):
                    n3 = tbl[decrypt_str[i]]
            i = i + 1
            if i <len(decrypt_str):
                if tbl.has_key(decrypt_str[i]):
                    n4 = tbl[decrypt_str[i]]
            i = i + 1

            sa.append(n1 << 2 | n2 >> 4)
            sa.append((15 & n2) << 4 | n3 >> 2)
            sa.append((3 & n3) << 6 | n4)
        e2 = decrypt_str[-2:]
        ## 这里没有判断类型是否相等，因为pad始终是None
        if e2[0] == pad:
            sa = sa[:-2]
        else:
            if e2[1] == pad:
                sa = sa[:-1]
        return xtoy(sa)
