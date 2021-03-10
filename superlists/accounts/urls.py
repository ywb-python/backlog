#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/3/7 11:17
# @Author  : ywb
# @Site    : 
# @File    : urls.py
# @Software: PyCharm


from django.conf.urls import url
from accounts import views
from django.contrib.auth import logout


urlpatterns = [
    url(r'^send_login_email$', views.send_login_email, name='send_login_email'),
    url(r'^login$', views.login, name='login'),
    url(r'^logout$', logout, {'next_page': '/'}, name='logout'),
]