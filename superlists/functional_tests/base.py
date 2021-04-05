#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/2/28 16:55
# @Author  : ywb
# @Site    : 
# @File    : base.py
# @Software: PyCharm


from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
import sys
import time
import os
from .server_tools import reset_database
from selenium.webdriver.common.keys import Keys
from .server_tools import create_session_on_server
from .management.commands.create_session import create_pre_authenticated_sessions
from django.conf import settings


MAX_WAIT = 10


def wait(fn):
    """
    等待页面出现某个事件
    :param fn: 期望事件
    :return: 返回事件的内容
    """

    def modified_fn(*args, **kwargs):
        start_time = time.time()
        while True:
            try:
                return fn(*args, **kwargs)
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    return modified_fn


class FunctionalTest(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        for arg in sys.argv:
            if 'liveserver' in arg:
                cls.server_url = 'http://' + arg.split('=')[1]
                return
        super().setUpClass()
        cls.server_url = cls.live_server_url

    def setUp(self):
        self.browser = webdriver.Chrome()
        self.staging_server = os.environ.get('STAGING_SERVER')
        if self.staging_server:
            self.live_server_url = 'http://' + self.staging_server
            reset_database(self.staging_server)

    def tearDown(self):
        self.browser.quit()

    @wait
    def wait_for(self, fn):
        """
        等待页面出现某个事件
        :param fn: 期望事件
        :return: 返回事件的内容
        """
        return fn()

    @wait
    def wait_for_row_in_list_table(self, row_text):
        """
        循环等待检测页面是否出现待检测文本
        :param row_text: 待检测文本
        """
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def get_item_input_box(self):
        """
        定位输入框
        """
        return self.browser.find_element_by_id('id_text')

    @wait
    def wait_to_be_logged_in(self, email):
        """
        等待登录成功
        :param email: 邮箱
        """
        self.browser.find_element_by_link_text('Log out')
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertIn(email, navbar.text)

    @wait
    def wait_to_be_logged_out(self, email):
        """
        等待登出成功
        :param email: 邮箱
        """
        self.browser.find_element_by_name('email')
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertNotIn(email, navbar.text)

    def add_list_item(self, item_text):
        """
        在输入框中输入文本
        :param item_text: 文本
        """
        num_rows = len(self.browser.find_elements_by_css_selector('#id_list_table tr'))
        self.get_item_input_box().send_keys(item_text)
        self.get_item_input_box().send_keys(Keys.ENTER)
        item_number = num_rows + 1
        self.wait_for_row_in_list_table(f'{item_number}: {item_text}')

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
