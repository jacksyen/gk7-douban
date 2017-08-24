#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
author by jacksyen[hyqiu.syen@gmail.com]
https://img1.doubanio.com/dae/staticng/s/ark/latest/js/dist/reader/0.a87ddde43dbddd68cc96.js

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

        _hex_chs = 'PQXVprI$7FzoK_S6aTCtj5nDexURy4NY9v03Wlu1iqsOJGEwfBmL2dhk8cgZMAbH'
        n = {}
        o = "~"
        a = 64
        for i in range(a):
            n[_hex_chs[i]] = i
        n1 = n2 = n3 = n4 = sa = []
        i = c = 0
        while i<len(decrypt_str):
            n1 = n2 = n3 = n4 = 0
            if n.has_key(decrypt_str[i]):
                n1 = n[decrypt_str[i]]
            i = i + 1
            if i <len(decrypt_str):
                if n.has_key(decrypt_str[i]):
                    n2 = n[decrypt_str[i]]
            i = i + 1
            if i <len(decrypt_str):
                if n.has_key(decrypt_str[i]):
                    n3 = n[decrypt_str[i]]
            i = i + 1
            if i <len(decrypt_str):
                if n.has_key(decrypt_str[i]):
                    n4 = n[decrypt_str[i]]
            i = i + 1

            sa.append(n1 << 2 | n2 >> 4)
            sa.append((15 & n2) << 4 | n3 >> 2)
            sa.append((3 & n3) << 6 | n4)
        e2 = decrypt_str[-2:]
        ## 这里没有判断类型是否相等，因为pad始终是None
        if e2[0] == o:
            sa = sa[:-2]
        else:
            if e2[1] == o:
                sa = sa[:-1]
        return xtoy(sa)
