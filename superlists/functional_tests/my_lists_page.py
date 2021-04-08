#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/4/8 23:06
# @Author  : ywb
# @Site    : 我的清单列表页面
# @File    : my_lists_page.py
# @Software: PyCharm


class MyListsPage(object):
    """
    我的清单列表页面
    """

    def __init__(self, test):
        self.test = test

    def go_to_my_lists_page(self):
        self.test.browser.get(self.test.live_server_url)
        self.test.browser.find_element_by_link_text('My lists').click()
        self.test.wait_for(lambda: self.test.assertEqual(
            self.test.browser.find_element_by_tag_name('h1').text,
            'My lists'
        ))
        return self