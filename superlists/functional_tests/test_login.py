#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/4/1 23:06
# @Author  : ywb
# @Site    : 登录相关的测试
# @File    : test_login.py
# @Software: PyCharm


from django.core import mail
from selenium.webdriver.common.keys import Keys
import re
from .base import FunctionalTest


TEST_EMAIL = '18721706546@163.com'
SUBJECT = 'Your login link for Superlists'


class LoginTest(FunctionalTest):
    """
    登录测试
    """

    def test_can_get_email_link_to_login_in(self):
        """
        测试点击邮件链接进行登录
        """
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_name('email').send_keys(TEST_EMAIL)
        self.browser.find_element_by_name('email').send_keys(Keys.ENTER)
        self.wait_for(lambda: self.assertIn(
            "Check your email", self.browser.find_element_by_tag_name('body').text
        ))
        email = mail.outbox[0]
        self.assertIn(TEST_EMAIL, email.to)
        self.assertEqual(email.subject, SUBJECT)
        self.assertIn('Use this link to log in', email.body)
        url_search = re.search(r'http://.+/.+$', email.body)
        if not url_search:
            self.fail(f'Could not find url in email body:\n{email.body}')
        url = url_search.group(0)
        self.assertIn(self.live_server_url, url)
        self.browser.get(url)
        self.wait_to_be_logged_in(email=TEST_EMAIL)
        self.browser.find_element_by_link_text('Log out').click()
        self.wait_to_be_logged_out(email=TEST_EMAIL)

