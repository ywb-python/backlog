#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/3/27 20:42
# @Author  : ywb
# @Site    : 表单组件的测试
# @File    : test_forms.py
# @Software: PyCharm
import self as self
from django.test import TestCase
from lists.forms import DUPLICATE_ITEM_ERROR, EMPTY_ITEM_ERROR, ExistingListItemForm, ItemForm
from lists.models import Item, List


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
        self.assertEqual(form.errors['text'], [EMPTY_ITEM_ERROR])


    def test_form_save_handles_saving_to_a_list(self):
        """
        测试待办事项是否保存到订单中
        """
        list_ = List.objects.create()
        form = ItemForm(data={"text": "do me"})
        new_item = form.save(for_list=list_)
        self.assertEqual(new_item, Item.objects.first())
        self.assertEqual(new_item.text, 'do me')
        self.assertEqual(new_item.list, list_)


class ExistingListItemFormTest(TestCase):
    """
    ExistingListItemForm类的测试
    """

    def test_form_renders_item_text_input(self):
        """
        测试form表单输入框的渲染情形
        """
        list_ = List.objects.create()
        form = ExistingListItemForm(for_list=list_)
        self.assertIn('placeholder="Enter a to-do item"', form.as_p())

    def test_form_validation_for_blank_items(self):
        """
        测试空待办事项提交失败
        """
        list_ = List.objects.create()
        form = ExistingListItemForm(for_list=list_, data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [EMPTY_ITEM_ERROR])

    def test_form_validation_for_duplicate_items(self):
        """
        测试重复待办事项提交失败
        """
        list_ = List.objects.create()
        Item.objects.create(list=list_, text='no twins!')
        form = ExistingListItemForm(for_list=list_, data={'text': 'no twins!'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [DUPLICATE_ITEM_ERROR])

    def test_form_save(self):
        """
        测试form表单的保存
        """
        list_ = List.objects.create()
        form = ExistingListItemForm(for_list=list_, data={'text':'hi'})
        new_item = form.save()
        self.assertEqual(new_item, Item.objects.all()[0])
