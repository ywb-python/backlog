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


    def test_logged_in_users_lists_are_saved_as_my_lists(self):
        """
        检查新创建的包含多个待办事项的清单会出现在列表页，并且以第一个待办事项命名
        """
        self.create_pre_authenticated_session('18721706546@163.com')
        self.browser.get(self.live_server_url)
        self.add_list_item('Reticulate splines')
        self.add_list_item('Immanentize eschaton')
        first_list_url = self.browser.current_url
        self.browser.find_element_by_link_text('My lists').click()
        self.wait_for(
            lambda: self.browser.find_element_by_link_text('Reticulate splines')
        )
        self.browser.find_element_by_link_text('Reticulate splines').click()
        self.wait_for(
            lambda: self.assertEqual(self.browser.current_url, first_list_url)
        )
        self.browser.get(self.live_server_url)
        self.add_list_item('Click cows')
        second_list_url = self.browser.current_url
        self.browser.find_element_by_link_text('My lists').click()
        self.wait_for(
            lambda: self.browser.find_element_by_link_text('Click cows')
        )
        self.browser.find_element_by_link_text('Click cows').click()
        self.wait_for(
            lambda: self.assertEqual(self.browser.current_url, second_list_url)
        )
        self.browser.find_element_by_link_text('Log out').click()
        self.wait_for(
            lambda: self.assertEqual(self.browser.find_element_by_link_text('My lists'), []
                                     ))
