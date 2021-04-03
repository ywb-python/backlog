#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/4/1 23:10
# @Author  : ywb
# @Site    : 模型测试
# @File    : test_models.py
# @Software: PyCharm


from django.test import TestCase
from django.contrib.auth import get_user_model
from accounts.models import Token
from django.contrib import auth


User = get_user_model()


class UserModelTest(TestCase):
    """
    模型User的测试
    """

    def test_user_is_valid_with_email_only(self):
        """
        测试只有一个邮箱信息的用户是否合法
        """

        user = User(email='18721706546@163.com')
        user.full_clean()

    def test_email_is_primary_key(self):
        """
        测试设置email字段为主键时的情形
        """
        user = User(email='18721706546@163.com')
        self.assertEqual(user.pk, '18721706546@163.com')

    def test_no_problem_with_auth_login(self):
        """
        测试认证登录有没有问题
        """
        user = User.objects.create(email='18721706546@163.com')
        user.backend = ''
        request = self.client.request().wsgi_request
        auth.login(request, user)


class TokenModelTest(TestCase):
    """
    模型Token的测试
    """

    def test_links_user_with_auto_generated_uid(self):
        """
        测试邮件地址每次是否可以关联到唯一的uid,
        """
        token1 = Token.objects.create(email='18721706546@163.com')
        token2 = Token.objects.create(email='18721706546@163.com')
        self.assertNotEqual(token1.uid, token2.uid)