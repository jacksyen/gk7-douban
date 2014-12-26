#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
author by jacksyen[hyqiu.syen@gmail.com]
---------------------------------------
后台管理登录
"""
import web

class Login:

    def __init__(self):
        self.render = web.template.render('templates', base='layout')

    def GET(self):
        return self.render.login()
