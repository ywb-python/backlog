#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/3/1 23:05
# @Author  : ywb
# @Site    : 视图函数的测试
# @File    : test_views.py
# @Software: PyCharm


import unittest
from unittest.mock import patch, Mock
from django.contrib.auth import get_user_model
from django.http import HttpRequest
from django.test import TestCase
from django.utils.html import escape

from lists.forms import (
    DUPLICATE_ITEM_ERROR, EMPTY_ITEM_ERROR,
    ExistingListItemForm, ItemForm,
)
from lists.models import Item, List
from lists.views import new_list


User = get_user_model()


class HomePageTest(TestCase):
    """
    视图函数home_page的单元测试
    """

    def test_uses_home_template(self):
        """
        测试网站根路径("/")能否被正确解析，映射到对应的视图函数上
        """
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_home_page_uses_item_form(self):
        """
        检查首页使用的表单类型是否正确
        """
        response = self.client.get('/')
        # assertIsInstance：表单是否属于正确的类
        self.assertIsInstance(response.context['form'], ItemForm)


class NewListViewIntegratedTest(TestCase):
    """
    视图函数new_list的单元测试
    """

    def test_can_save_a_POST_request(self):
        """
        测试首页能否处理post请求并成功保存其内容
        """
        self.client.post('/lists/new', data={'text': 'A new list item'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')


    def test_for_invalid_input_doesnt_save_but_shows_errors(self):
        """
        测试提交空待办事项时响应码是否正确以及首页是否被渲染
        """
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertEqual(List.objects.count(), 0)
        self.assertContains(response, escape(EMPTY_ITEM_ERROR))


    def test_list_owner_is_saved_if_user_is_authenticated(self):
        """
        测试已登录用户能否将新建的清单指派到自己名下
        """
        user = User.objects.create(email='a@b.com')
        self.client.force_login(user)
        self.client.post('/lists/new', data={'text': 'new item'})
        list_ = List.objects.first()
        self.assertEqual(list_.owner, user)



@patch('lists.views.NewListForm')
class NewListViewUnitTest(unittest.TestCase):
    """
    视图函数new_list的单元测测试
    """

    def setUp(self):
        self.request = HttpRequest()
        self.request.POST['text'] = 'new list item'
        self.request.user = Mock()

    def test_passes_POST_data_to_NewListForm(self, mockNewListForm):
        """
        测试能否正确读取请求中携带的参数
        :param mockNewListForm: NewListForm模拟表单
        """
        new_list(self.request)
        mockNewListForm.assert_called_once_with(data=self.request.POST)

    def test_saves_form_with_owner_if_form_valid(self, mockNewListForm):
        """
        测试合理的表单时否可以保存在属主名下
        :param mockNewListForm:NewListForm模拟表单
        """
        mock_form = mockNewListForm.return_value
        mock_form.is_valid.return_value = True
        new_list(self.request)
        mock_form.save.assert_called_once_with(owner=self.request.user)

    def test_does_not_save_if_form_invalid(self, mockNewListForm):
        mock_form = mockNewListForm.return_value
        mock_form.is_valid.return_value = False
        new_list(self.request)
        self.assertFalse(mock_form.save.called)
    @patch('lists.views.redirect')
    def test_redirects_to_form_returned_object_if_form_valid(
        self, mock_redirect, mockNewListForm
    ):
        """
        测试表单数据有效情形下的重定向
        :param mock_redirect: 模拟的redirect函数
        :param mockNewListForm: NewListForm模拟表单
        """
        mock_form = mockNewListForm.return_value
        mock_form.is_valid.return_value = True
        response = new_list(self.request)
        self.assertEqual(response, mock_redirect.return_value)
        mock_redirect.assert_called_once_with(mock_form.save.return_value)

    @patch('lists.views.render')
    def test_renders_home_template_with_form_if_form_invalid(self, mock_render, mockNewListForm):
        """
        测试表单数据有效情形下的首页渲染
        :param mock_render: 模拟的render函数
        :param mockNewListForm: NewListForm模拟表单
        """
        mock_form = mockNewListForm.return_value
        mock_form.is_valid.return_value = False

        response = new_list(self.request)
        self.assertEqual(response, mock_render.return_value)
        mock_render.assert_called_once_with(
            self.request, 'home.html', {'form': mock_form}
        )



class ListViewTest(TestCase):
    """
    视图函数view_list的单元测试
    """

    def test_uses_list_template(self):
        """
        测试网站根路径("/lists/{list_.id}/")能否被正确解析，映射到对应的视图函数上
        """
        list_ = List.objects.create()
        # 使用Django测试客户端
        response = self.client.get(f'/lists/{list_.id}/')
        # 检查使用的模板
        self.assertTemplateUsed(response, 'list.html')

    def test_passes_correct_list_to_template(self):
        """
        测试新提交的待办事项是否正确显示在对应的模板上
        """
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get(f'/lists/{correct_list.id}/')
        # 检查查询结果集里面都是正确的待办事项
        self.assertEqual(response.context['list'], correct_list)


    def test_displays_item_form(self):
        """
        测试待办事项清单页的显示
        """
        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.id}/')
        # 检查表单使用正确的类
        self.assertIsInstance(response.context['form'], ExistingListItemForm)
        self.assertContains(response, 'name="text"')


    def test_can_save_a_POST_request_to_an_existing_list(self):
        """
        测试新生成的待办事项有没有加入到现有的清单中
        """
        other_list = List.objects.create()
        correct_list = List.objects.create()
        self.client.post(
            f'/lists/{correct_list.id}/',
            data={"text": "A new item for an existing list"}
        )
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        # post的测试
        self.assertEqual(new_item.text, "A new item for an existing list")
        self.assertEqual(new_item.list, correct_list)

    def test_POST_redirects_to_list_view(self):
        """
        测试新提交待办事项后重定向的正确性
        """
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.post(
            f'/lists/{correct_list.id}/',
            data={"text": "A new item for an existing list"}
        )
        self.assertRedirects(response, f'/lists/{correct_list.id}/')

    def post_invalid_input(self):
        """
        输入的待办事项为空时进行post提交
        """
        list_ = List.objects.create()
        return self.client.post(
            f'/lists/{list_.id}/',
            data={'text': ''}
        )

    def test_for_invalid_input_nothing_saved_to_db(self):
        """
        测试空的待办事项没有被保存到数据库
        """
        self.post_invalid_input()
        self.assertEqual(Item.objects.count(), 0)

    def test_for_invalid_input_renders_list_template(self):
        """
        测试提交空待办事项时响应码是否正确以及清单列表页是否被渲染
        """
        response = self.post_invalid_input()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list.html')

    def test_for_invalid_input_passes_form_to_template(self):
        """
        测试提交空待办事项时表单对象是否有传入清单列表页页模板
        """
        response = self.post_invalid_input()
        self.assertIsInstance(response.context['form'], ExistingListItemForm)

    def test_for_invalid_input_shows_error_on_page(self):
        """
        测试清单页的错误消息显示
        """
        response = self.post_invalid_input()
        # 检查是否渲染指定的表单， 而且显示错误消息
        self.assertContains(response, escape(EMPTY_ITEM_ERROR))

    def test_duplicate_item_validation_errors_end_up_on_lists_page(self):
        """
        测试待办事项重复提交时清单页错误消息的显示
        """
        list1 = List.objects.create()
        item1 = Item.objects.create(list=list1, text='textey')
        response = self.client.post(
            f'/lists/{list1.id}/',
            data={'text': 'textey'}
        )
        expected_error = escape(DUPLICATE_ITEM_ERROR)
        self.assertContains(response, expected_error)
        self.assertTemplateUsed(response, 'list.html')
        self.assertEqual(Item.objects.all().count(), 1)


class MyListsTest(TestCase):
    """
    视图函数my_lists的单元测试
    """

    def test_my_lists_url_renders_my_lists_template(self):
        """
        测试url:my_lists能否渲染my_lists模板
        """
        User.objects.create(email='a@b.com')
        response = self.client.get('/lists/users/a@b.com/')
        self.assertTemplateUsed(response, 'my_lists.html')

    def test_passes_correct_owner_to_template(self):
        """
        测试为每个用户展示自己对应的待办事项清单
        """
        User.objects.create(email='wrong@owner.com')
        correct_user = User.objects.create(email='a@b.com')
        response = self.client.get('/lists/users/a@b.com/')
        self.assertEqual(response.context['owner'], correct_user)
# Create your tests here.
