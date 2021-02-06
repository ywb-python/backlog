#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/2/6 20:41
# @Author  : ywb
# @Site    : 
# @File    : functional_tests.py
# @Software: PyCharm


from selenium import webdriver


browser = webdriver.Chrome()
browser.get('http://localhost:8000')
assert 'Django' in browser.title