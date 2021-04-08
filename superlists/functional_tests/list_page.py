#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/4/8 21:47
# @Author  : ywb
# @Site    : 页面对象
# @File    : list_page.py
# @Software: PyCharm


from selenium.webdriver.common.keys import Keys
from .base import wait


class ListPage(object):
    """
    页面对象类
    """

    def __init__(self, test):
        self.test = test

    def get_table_rows(self):
        """
        获取列表的所有行
        """
        return self.test.browser.find_elements_by_css_selector('#id_list_table tr')

    @wait
    def wait_for_row_in_list_table(self, item_text, item_number):
        """
        循环等待检测页面是否出现待检测文本
        :param item_text: 待检测文本
        :param item_number: 待检测文本所在行
        """
        expected_row_text = f'{item_number}: {item_text}'
        rows = self.get_table_rows()
        self.test.assertIn(expected_row_text, [row.text for row in rows])

    def get_item_input_box(self):
        """
        定位输入框
        """
        return self.test.browser.find_element_by_id('id_text')

    def add_list_item(self, item_text):
        """
        在输入框中输入文本
        :param item_text: 文本
        """
        new_item_no = len(self.get_table_rows()) + 1
        self.get_item_input_box().send_keys(item_text)
        self.get_item_input_box().send_kyes(Keys.ENTER)
        self.wait_for_row_in_list_table(item_text, new_item_no)
        return self

    def get_share_box(self):
        """
        获取分享按钮控件
        """
        return self.test.browser.find_elements_by_css_selector('input[name="sharee"]')

    def get_shared_with_list(self):
        """
        获取要分享的列表
        """
        return self.test.browser.find_elements_by_css_selector('.list-sharee')

    def share_list_with(self, email):
        """
        分享给指定用户
        :param email: 邮箱
        """
        self.get_share_box().send_keys(email)
        self.get_share_box().send_keys(Keys.ENTER)
        self.test.wait_for(lambda: self.test.assertIn(
            email, [item.text for item in self.get_shared_with_list()]
        ))

    def get_lists_owner(self):
        """
        获取订单列表的属主
        """
        return self.test.browser.find_element_by_id('id_list_owner').text
