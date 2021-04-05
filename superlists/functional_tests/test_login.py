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
import os
import poplib
import time
from ..superlists import settings


TEST_EMAIL = '18721706546@163.com'
SUBJECT = 'Your login link for Superlists'


class LoginTest(FunctionalTest):
    """
    登录测试
    """

    def wait_for_email(self, test_email, subject):
        """
        等待邮件
        :param test_email: 测试邮箱
        :param subject: 邮件主题
        """
        if not self.staging_server:
            email = mail.outbox[0]
            self.assertIn(test_email, email.to)
            self.assertEqual(email.subject, subject)
            return email.body
        email_id = None
        start = time.time()
        inbox = poplib.POP3_SSL('18721706546@163.com')
        try:
            inbox.user(test_email)
            inbox.pass_(settings.EMAIL_HOST_PASSWORD)
            while time.time() - start < 60:
                count, _ = inbox.stat()
                for i in reversed(range(max(1, count - 10), count + 1)):
                    print('getting msg', i)
                    _, lines, _ = inbox.retr(i)
                    lines = [l.decode('utf8') for l in lines]
                    print(lines)
                    if f'Subject: {subject}' in lines:
                        email_id = i
                        body = '\n'.join(lines)
                        return body
                time.sleep(5)
        finally:
            if email_id:
                inbox.dele(email_id)
            inbox.quit()

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
        body = self.wait_for_email(TEST_EMAIL, SUBJECT)
        self.assertIn('Use this link to log in', body)
        url_search = re.search(r'http://.+/.+$', body)
        if not url_search:
            self.fail(f'Could not find url in email body:\n{body}')
        url = url_search.group(0)
        self.assertIn(self.live_server_url, url)
        self.browser.get(url)
        self.wait_to_be_logged_in(email=TEST_EMAIL)
        self.browser.find_element_by_link_text('Log out').click()
        self.wait_to_be_logged_out(email=TEST_EMAIL)

