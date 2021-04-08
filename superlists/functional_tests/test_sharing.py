#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/4/8 21:28
# @Author  : ywb
# @Site    : 多用户测试
# @File    : test_sharing.py
# @Software: PyCharm


from selenium import webdriver
from .base import FunctionalTest
from .list_page import ListPage


def quit_if_prossible(browser):
    """
    浏览器关闭
    """
    try:
        browser.quit()
    except:
        pass


class SharingTest(FunctionalTest):
    """
    多用户测试
    """

    def test_can_share_a_list_with_another_user(self):
        """
        测试当前登录用户对其他用户有一个分析列表
        """
        self.create_pre_authenticated_session('edith@example.com')
        edit_browser = self.browser
        self.addCleanup(lambda: quit_if_prossible(edit_browser))
        oni_browser = webdriver.Chrome()
        self.addCleanup(lambda: quit_if_prossible(oni_browser))
        self.browser = oni_browser
        self.create_pre_authenticated_session('oniciferous@Eexample.com')
        self.browser = edit_browser
        list_page = ListPage(self).add_list_item('Get help')
        shared_box = list_page.get_share_box()
        self.assertEqual(shared_box.get_attribute('placeholder'), 'your-frined@example.com')
        list_page.share_list_with('oniciferous@example.com')


