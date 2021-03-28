#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/3/27 20:42
# @Author  : ywb
# @Site    : 表单组件的测试
# @File    : test_forms.py
# @Software: PyCharm


from django.test import TestCase
from lists.forms import EMPTY_ITEM_ERROR, ItemForm


class ItemFormTest(TestCase):
    """
    ItemForm类的测试
    """

    def test_form_item_input_has_placeholder_and_css_classes(self):
        """
        测试文本输入框的placeholder属性和css类
        """
        form = ItemForm()
        self.assertIn('placeholder="Enter a to-do item"', form.as_p())
        self.assertIn('class="form-control input-lg"', form.as_p())

    def test_form_validation_for_blank_items(self):
        """
        测试模型是否应用了模型中定义的验证规则
        """
        form = ItemForm(data={'text': ''})
        # form.is_valid():检查验证是否通过
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'],
                         [EMPTY_ITEM_ERROR])
