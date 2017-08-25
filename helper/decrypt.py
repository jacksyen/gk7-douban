#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
author by jacksyen[hyqiu.syen@gmail.com]
https://img1.doubanio.com/dae/staticng/s/ark/latest/js/dist/reader/0.a87ddde43dbddd68cc96.js

key = $("#tmpl-id").attr('id').split("").reverse()
i = 53092
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
    def parse(tmpl_id, denum, decrypt_str):
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


        def ioc(e):
            if type(e) == list:
                t = 0
                n = []
                for i in range(len(e)):
                    n.append(e[i])
                    t = t+1
                return n
            return list(e)

        def oid(e, t, n=64):
            for i in t:
                r = ord(str(i)) % n
                x = ioc(e[r:])
                x.extend(ioc(e[:r]))
                e = x
            return e
        #'PQXVprI$7FzoK_S6aTCtj5nDexURy4NY9v03Wlu1iqsOJGEwfBmL2dhk8cgZMAbH'
        _hex_chs = oid(str(tmpl_id), denum)
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

'''
function(t, e, i) {
    function n(t) {
        if (Array.isArray(t)) {
            for (var e = 0, i = Array(t.length); e < t.length; e++)
                i[e] = t[e];
            return i
        }
        return Array.from(t)
    }
    function o(t, e, i) {
        var n = {}
          , o = String.fromCharCode("}".charCodeAt(0) + 1)
          , a = e.length;
        e = s(e, i, a);
        for (var l = 0; l < a; ++l)
            n[e[l]] = l;
        for (var h, c, d, u, p = [], f = 0, g = 0; f < t.length; )
            h = n[t[f++]],
            c = n[t[f++]],
            d = n[t[f++]],
            u = n[t[f++]],
            p[g++] = h << 2 | c >> 4,
            p[g++] = (15 & c) << 4 | d >> 2,
            p[g++] = (3 & d) << 6 | u;
        var m = t.slice(-2);
        return m[0] === o ? p.length = p.length - 2 : m[1] === o && (p.length = p.length - 1),
        r(p)
    }
    function r(t) {
        for (var e = "", i = 0; i < t.length; ++i) {
            var n = t[i];
            e += String.fromCharCode(256 * n + t[++i])
        }
        return e
    }
    function s(t, e, i) {
        return e ? (t = t.slice(),
        e.split("").forEach(function(e) {
            var o = e.charCodeAt(0) % i;
            t = [].concat(n(t.slice(o)), n(t.slice(0, o)))
        }),
        t) : t
    }
    var a = i(32);
    t.exports = function(t, e) {
        return o(t, a, e)
    }
}
'''
