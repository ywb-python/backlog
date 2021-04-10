# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/2/6 20:41
# @Author  : ywb
# @Site    : 使用unittest模块组织测试类
# @File    : functional_tests.py
# @Software: PyCharm


from selenium import webdriver
import unittest


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        """
        测试首页标题的正确性
        """
        self.browser.get('http://localhost:8000')
        self.assertIn('To-Do', self.browser.title)
        self.fail('Finish the test!')


if __name__ == '__main__':
    # warnings='ignore'：禁止抛出异常
    unittest.main(warnings='ignore')