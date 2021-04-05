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
from .management.commands.create_session import create_pre_authenticated_sessions
from .server_tools import create_session_on_server


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
        if self.staging_server:
            session_key = create_session_on_server(self.staging_server, email)
        else:
            session_key = create_pre_authenticated_sessions(email)
        self.browser.get(self.live_server_url + "/404_no_such_url/")
        self.browser.add_cookie(dict(name=settings.SESSION_COOKIE_NAME, value=session_key, path='/'))
        user = User.objects.create(email=email)
        session = SessionStore()
        session[SESSION_KEY] = user.pk
        session[BACKEND_SESSION_KEY] = settings.AUTHENTICtion_BACKENDS[0]
        session.save()
        self.browser.add_cookie(dict(name=settings.SESSION_COOKIE_NAME, value=session.session_key,
                                     path='/'))