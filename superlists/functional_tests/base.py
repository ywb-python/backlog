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
from datetime import datetime
from .server_tools import create_session_on_server
from django.conf import settings
from .management.commands.create_session import create_pre_authenticated_session


MAX_WAIT = 10
SCREEN_DUMP_LOCATION = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'screendumps')


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
        if self._test_has_failed():
            if not os.path.exists(SCREEN_DUMP_LOCATION):
                os.makedirs(SCREEN_DUMP_LOCATION)
            for ix, handle in enumerate(self.browser.window_handles):
                self._windowid = ix
                self.browser.switch_to_window(handle)
                self.take_screenshot()
                self.dump_html()
        self.browser.quit()
        super().tearDown()

    def _test_has_failed(self):
        """
        检测是否有失败并返回失败的详情
        """
        return any(error for (method, error) in self._outcome.errors)

    def take_screenshot(self):
        """
        进行截图并进行保存
        """
        filename = self._get_filename() + '.jpg'
        print('screentshotting to', filename)
        self.browser.get_screenshot_as_file(filename)

    def dump_html(self):
        """
        传输HTML网页
        """
        filename = self._get_filename() + '.html'
        print('dumping page HTML to', filename)
        with open(filename, 'w') as f:
            f.write(self.browser.page_source)

    def _get_filename(self):
        """
        获取文件名
        """
        timestamp = datetime.now().isoformat().replace(':', '.')[:19]
        return '{folder}/{classname}.{method}-window{windowid}-{timestamp}'.format(
            folder = SCREEN_DUMP_LOCATION,
            classname=self.__class__.__name__,
            method=self._testMethodName,
            windowid=self._windowid,
            timestamp=timestamp
        )




    @wait
    def wait_for(self, fn):
        """
        等待页面出现某个事件
        :param fn: 期望事件
        :return: 返回事件的内容
        """
        return fn()


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

    def create_pre_authenticated_session(self, email):
        if self.staging_server:
            session_key = create_session_on_server(self.staging_server, email)
        else:
            session_key = create_pre_authenticated_session(email)

        ## to set a cookie we need to first visit the domain.
        ## 404 pages load the quickest!
        self.browser.get(self.live_server_url + "/404_no_such_url/")
        self.browser.add_cookie(dict(
            name=settings.SESSION_COOKIE_NAME,
            value=session_key,
            path='/',
        ))
