#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/3/1 23:05
# @Author  : ywb
# @Site    : 视图函数的测试
# @File    : test_views.py
# @Software: PyCharm


from django.test import TestCase
from lists.models import Item, List
from django.utils.html import escape
from lists.forms import EMPTY_ITEM_ERROR


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


class NewListTest(TestCase):
    """
    视图函数new_list的单元测试
    """

    def test_can_save_a_POST_request(self):
        """
        测试首页能否处理post请求并成功保存其内容
        """
        self.client.post('/lists/new', data={'item_text': 'A new list item'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_POST(self):
        """
        测试首页处理完post请求之后的重定向是否正确
        """
        response = self.client.post('/lists/new', data={'item_text': 'A new list item'})
        new_list = List.objects.first()
        self.assertRedirects(response, f'/lists/{new_list.id}/')

    def test_validation_errors_are_sent_back_to_home_page_template(self):
        """
        测试错误消息显示在首页中
        """
        response = self.client.post('/lists/new', data={'item_text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        expected_error = escape(EMPTY_ITEM_ERROR)
        self.assertContains(response, expected_error)

    def test_validtaion_list_items_arent_saved(self):
        """
        测试空待办事项不会被保存
        """
        self.client.post('/lists/new', data={'item_text': ''})
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(List.objects.count(), 0)


class ListViewTest(TestCase):
    """
    视图函数view_list的单元测试
    """

    def test_uses_list_template(self):
        """
        测试网站根路径("/lists/{list_.id}/")能否被正确解析，映射到对应的视图函数上
        """
        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.id}/')
        self.assertTemplateUsed(response, 'list.html')

    def test_passes_correct_list_to_template(self):
        """
        测试新提交的待办事项是否正确显示在对应的模板上
        """
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get('/lists/%d/' % (correct_list.id,))
        self.assertEqual(response.context['list'], correct_list)

    def test_displays_only_items_for_that_list(self):
        """
        测试是否可以显示对应List对象下的所有待办事项
        """
        correct_list = List.objects.create()
        Item.objects.create(text='itemey 1', list=correct_list)
        Item.objects.create(text='itemey 2', list=correct_list)
        other_list = List.objects.create()
        Item.objects.create(text='other list item 1', list=other_list)
        Item.objects.create(text='other list item 2', list=other_list)
        response = self.client.get(f'/lists/{correct_list.id}/')
        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
        self.assertNotContains(response, 'other list item 1')
        self.assertNotContains(response, 'other list item 2')

    def test_can_save_a_POST_request_to_an_existing_list(self):
        """
        测试新生成的待办事项有没有加入到现有的清单中
        """
        other_list = List.objects.create()
        correct_list = List.objects.create()
        self.client.post(
            f'/lists/{correct_list.id}/',
            data={"item_text": "A new item for an existing list"}
        )
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
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
            data={"item_text": "A new item for an existing list"}
        )
        self.assertRedirects(response, f'/lists/{correct_list.id}/')

    def test_validation_errors_end_up_on_lists_page(self):
        """
        测试清单页的错误消息显示
        """
        list_ = List.objects.create()
        response = self.client.post(f'/lists/{list_.id}/', data = {'item_text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list.html')
        expected_error = escape(EMPTY_ITEM_ERROR)
        self.assertContains(response, expected_error)

# Create your tests here.
