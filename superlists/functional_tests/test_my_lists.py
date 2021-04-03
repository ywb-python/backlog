#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/4/3 22:34
# @Author  : ywb
# @Site    : 我的待办事项清单相关的测试
# @File    : test_my_lists.py
# @Software: PyCharm


from django.conf import settings
from django.contrib.auth import BACKEND_SESSION_KEY, SESSION_KEY, get_user_model
from django.contrib.sessions.backends.db import SessionStore
from .base import FunctionalTest


User = get_user_model()


class MyListsTest(FunctionalTest):
    """
    我的待办事项清单相关的测试
    """
    def create_pre_authenticated_session(self, email):
        """
        产生认证后的session信息
        :param email: 用户邮箱
        """
        user = User.objects.create(email=email)
        session = SessionStore()
        session[SESSION_KEY] = user.pk
        session[BACKEND_SESSION_KEY] = settings.AUTHENTICtion_BACKENDS[0]
        session.save()
        self.browser.add_cookie(dict(name=settings.SESSION_COOKIE_NAME, value=session.session_key,
                                     path='/'))