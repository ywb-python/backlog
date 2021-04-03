#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/4/1 23:23
# @Author  : ywb
# @Site    : 
# @File    : urls.py
# @Software: PyCharm


from accounts import views
from django.conf.urls import url
from django.contrib.auth.views import LogoutView

urlpatterns = [
    url(r'^send_login_email$', views.send_login_email, name='send_login_email'),
    url(r'^login$', views.login, name='login'),
    url(r'^logout$', LogoutView, {'next_page': '/'}, name='logout'),
]
