#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/3/27 20:42
# @Author  : ywb
# @Site    : 表单组件的测试
# @File    : test_forms.py
# @Software: PyCharm


from django.test import TestCase
from lists.forms import DUPLICATE_ITEM_ERROR, EMPTY_ITEM_ERROR, ExistingListItemForm, ItemForm, NewListForm
from lists.models import Item, List
from unittest.mock import patch, Mock
import unittest
from django.contrib.auth import get_user_model


User = get_user_model()


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


class NewListFormTest(unittest.TestCase):
    """
    模型NewListForm的测试
    """

    @patch('lists.views.List')
    @patch('lists.views.Item')
    def test_save_creates_new_list_and_item_from_post_data(self, mockItem, mockList):
        """
        测试每一个新的待办事项都会产生一个新的清单列表
        :param mockItem: Item模拟模型
        :param mockList: List模拟模型
        """
        mock_item = mockItem.return_value
        mock_list = mockList.return_value
        user = Mock()
        form = NewListForm(data={'text': 'new item text'})
        form.is_valid()

        def check_item_text_and_list():
            self.assertEqual(mock_item.text, 'new item text')
            self.assertEqual(mock_item.list, mock_list)
            self.assertTrue(mock_list.save.called)

        mock_item.save.side_effect = check_item_text_and_list
        form.save(owner=user)
        self.assertTrue(mock_item.save.called)

    @patch('lists.forms.List.create_new')
    def test_save_create_new_list_from_post_data_if_user_not_authenticated(self, mock_List_create_new):
        """
        测试未认证用户可以通过post请求产生一个新的待办事项清单列表
        :param mock_List_create_new: 模拟的清单生成方法
        """
        user = Mock(is_authenticated=False)
        form = NewListForm(data={'text': 'new item text'})
        form.is_valid()
        form.save(owner=user)
        mock_List_create_new.assert_called_once_with(
            first_item_text='new item text'
        )

    @patch('lists.forms.List.create_new')
    def test_save_create_new_list_from_post_data_if_user_authenticated(self, mock_List_create_new):
        """
        测试未认证用户可以通过post请求产生一个新的待办事项清单列表
        :param mock_List_create_new: 模拟的清单生成方法
        """
        user = Mock(is_authenticated=True)
        form = NewListForm(data={'text': 'new item text'})
        form.is_valid()
        form.save(owner=user)
        mock_List_create_new.assert_called_once_with(
            first_item_text='new item text', owner=user
        )

    @patch('lists.forms.List.create_new')
    def test_save_return_new_list_object(self, mock_List_create_new):
        """
        测试未认证用户可以通过post请求产生一个新的待办事项清单列表
        :param mock_List_create_new: 模拟的清单生成方法
        """
        user = Mock(is_authenticated=True)
        form = NewListForm(data={'text': 'new item text'})
        form.is_valid()
        response = form.save(owner=user)
        self.assertEqual(response, mock_List_create_new.return_value)

    def test_create_returns_new_list_object(self):
        """
        测试产生返回一个新的清单列表
        """
        self.fail()