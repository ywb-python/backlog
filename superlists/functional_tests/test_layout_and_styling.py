#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/2/28 16:56
# @Author  : ywb
# @Site    : 
# @File    : test_layout_and_styling.py
# @Software: PyCharm


from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest


class LayoutAndStylingTest(FunctionalTest):

    def test_layout_and_styling(self):
        """
        测试页面布局
        """
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)
        # assertAlmostEqual():帮助处理舍入误差以及偶尔由滚动条等事物导致的异常，这里制定计算结果在10像素范围内为可接受
        self.assertAlmostEqual(
            self.get_item_input_box().location['x'] + self.get_item_input_box().size['width'] / 2,
            512,
            delta=10
        )
        self.add_list_item('testing')
        self.assertAlmostEqual(
            self.get_item_input_box().location['x'] + self.get_item_input_box().size['width'] / 2,
            512,
            delta=10
        )
