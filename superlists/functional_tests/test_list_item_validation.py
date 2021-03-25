#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/2/28 16:56
# @Author  : ywb
# @Site    : 
# @File    : test_list_item_validation.py
# @Software: PyCharm


from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_list_items(self):
        self.browser.get(self.server_url)
        self.send_keys_to_item_input_box(Keys.ENTER)
        self.wait_for(lambda: self.assertEqual(self.browser.find_element_by_css_selector('.has-error').text,
                                               "You can't have an empty list item"))
        self.send_keys_to_item_input_box('Buy milk')
        self.send_keys_to_item_input_box(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')
        self.send_keys_to_item_input_box(Keys.ENTER)
        self.wait_for(lambda: self.assertEqual(self.browser.find_element_by_css_selector('.has-error').text,
                                               "You can't have an empty list item"))
        self.send_keys_to_item_input_box('Make tea')
        self.send_keys_to_item_input_box(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')
        self.wait_for_row_in_list_table('2: Make tea')
