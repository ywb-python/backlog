#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/2/28 16:56
# @Author  : ywb
# @Site    : 
# @File    : test_list_item_validation.py
# @Software: PyCharm


from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest
from lists.forms import EMPTY_ITEM_ERROR, DUPLICATE_ITEM_ERROR


class ItemValidationTest(FunctionalTest):
    """
    待办事项提交异常的测试
    """
    def test_cannot_add_empty_list_items(self):
        """
        测试不能提交空的待办事项
        """
        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for(lambda: self.browser.find_elements_by_css_selector('#id_text:invalid'))
        self.get_item_input_box().send_keys('Buy milk')
        self.wait_for(lambda: self.browser.find_elements_by_css_selector('#id_text:invalid'))
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')
        self.wait_for(lambda: self.browser.find_elements_by_css_selector('#id_text:invalid'))
        self.get_item_input_box().send_keys('Make tea')
        self.wait_for(lambda: self.browser.find_elements_by_css_selector('#id_text:invalid'))
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')
        self.wait_for_row_in_list_table('2: Make tea')

    def test_cannot_add_duplicate_items(self):
        """
        测试不能提交重复的待办事项
        """
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys('Buy wellies')
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy wellies')
        self.get_item_input_box().send_keys('Buy wellies')
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_css_selector('.has-error').text, DUPLICATE_ITEM_ERROR))
