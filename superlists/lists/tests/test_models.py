#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/3/1 23:05
# @Author  : ywb
# @Site    : 模型的测试
# @File    : test_models.py
# @Software: PyCharm


from django.test import TestCase
from django.core.exceptions import ValidationError
from lists.models import Item, List
from django.contrib.auth import get_user_model


User = get_user_model()


class ItemModelsTest(TestCase):
    """
    模型Item的单元测试
    """
    def test_default_text(self):
        """
        测试待办事项text字段的默认显示
        """
        item = Item()
        self.assertEqual(item.text, '')

    def test_item_is_related_to_list(self):
        """
        测试新建List对象名下的待办事项能否被正确保存
        """
        list_ = List.objects.create()
        item = Item()
        item.list = list_
        item.save()
        self.assertIn(item, list_.item_set.all())

    def test_cannot_save_empty_list_items(self):
        """
        测试一个空的待办事项模型不能保存
        """
        list_ = List.objects.create()
        item = Item(list=list_, text='')
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()

    def test_duplicate_items_are_invalid(self):
        """
        测试禁止向同一清单中提交重复的待办事项
        """
        list_ = List.objects.create()
        Item.objects.create(list=list_, text='bla')
        with self.assertRaises(ValidationError):
            item = Item(list=list_, text='bla')
            item.full_clean()

    def test_CAN_save_same_item_to_different_lists(self):
        """
        测试允许向不同清单中提交重复的待办事项
        """
        list1 = List.objects.create()
        list2 = List.objects.create()
        Item.objects.create(list=list1, text='bla')
        item = Item(list=list2, text='bla')
        item.full_clean()

    def test_list_ordering(self):
        """
        测试多个待办事项的排序
        """
        list1 = List.objects.create()
        item1 = Item.objects.create(list=list1, text='i1')
        item2 = Item.objects.create(list=list1, text='item 2')
        item3 = Item.objects.create(list=list1, text='3')
        self.assertEqual(
            list(Item.objects.all()),
            [item1, item2, item3]
        )

    def test_string_representation(self):
        """
        测试待办事项的字符串的表示形式
        """
        item = Item(text='some text')
        self.assertEqual(str(item), 'some text')


class ListModelTest(TestCase):
    """
    模型List单元测试
    """
    def test_get_absolute_url(self):
        """
        测试url解析
        """
        list_ = List.objects.create()
        self.assertEqual(list_.get_absolute_url(), f'/lists/{list_.id}/')

    def test_lists_can_have_owners(self):
        """
        测试待办事项可以拥有属主
        """
        List(owner=User())

    def test_list_owner_is_optional(self):
        """
        测试属主是一个可有可无的属性
        """
        List().full_clean()

    def test_list_name_is_first_item_text(self):
        """
        测试清单列表的名字是不是以第一个待办事项命名的
        """
        list_ = List.objects.create()
        Item.objects.create(list=list_, text='first item')
        Item.objects.create(list=list_, text='second item')
        self.assertEqual(list_.name, 'first item')
    def test_create_new_creates_list_and_first_item(self):
        """
        测试产生一个新的待办事项和列表清单
        """
        List.create_new(first_item_text='new item text')
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'new item text')
        new_list = List.objects.first()
        self.assertEqual(new_item.list, new_list)

    def test_create_new_optionally_saves_owner(self):
        """
        测试清单有一个属主选项
        """
        user = User.objects.create()
        List.create_new(first_item_text='new item text', owner=user)
        new_list = List.objects.first()
        self.assertEqual(new_list.owner, user)

    def test_create_returns_new_list_object(self):
        """
        测试生成并返回一个新的清单列表对象
        """
        returned = List.create_new(first_item_text='new item text')
        new_list = List.objects.first()
        self.assertEqual(returned, new_list)


