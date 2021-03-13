#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/2/27 19:25
# @Author  : ywb
# @Site    : 
# @File    : urls.py
# @Software: PyCharm


from lists import views
from django.conf.urls import url


urlpatterns = [
    url(r'^new$', views.new_list, name='new_list'),
    url(r'^(\d+)/$', views.view_list, name='view_list'),
    url(r'^(\d+)/share$', views.share_list, name='share_list'),
    url(r'^users/(.+)/$', views.my_lists, name='my_lists'),
]

