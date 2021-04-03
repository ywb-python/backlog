#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/4/3 15:59
# @Author  : ywb
# @Site    : 测试身份验证效果
# @File    : test_authentication.py
# @Software: PyCharm


from django.test import TestCase
from django.contrib.auth import get_user_model
from accounts.authentication import PasswordlessAuthenticationBackend
from accounts.models import Token


User = get_user_model()


class AuthenticateTest(TestCase):

    """
    用户身份验证测试
    """

    def test_returns_None_if_no_such_token(self):
        """
        测试没有获取到用户的uid信息时返回None
        """
        result = PasswordlessAuthenticationBackend().authenticate('no-such-token')
        self.assertIsNone(result)

    def test_returns_new_user_with_correct_email_if_token_exists(self):
        """
        测试获取到用户uid时数据库没有该用户时则创建一个新用户并返回这个新用户
        """
        email = '18721706546@163.com'
        token = Token.objects.create(email=email)
        user = PasswordlessAuthenticationBackend().authenticate(token.uid)
        new_user = User.objects.get(email=email)
        self.assertEqual(user, new_user)

    def test_returns_existing_user_with_correct_email_if_token_exists(self):
        """
        测试获取到用户uid时数据库存在该用户时则创直接返回该用户
        """
        email = '1718951687@163.com'
        existing_user = User.objects.create(email=email)
        token = Token.objects.create(email=email)
        user = PasswordlessAuthenticationBackend().authenticate(token.uid)
        self.assertEqual(user, existing_user)


class GetUserTest(TestCase):
    """
    用户信息获取测试
    """
    def test_gets_user_by_email(self):
        """
        测试通过邮箱获取用户信息
        """
        User.objects.create(email='another@exaple.com')
        desirec_user = User.objects.create(email='edith@example.com')
        found_user = PasswordlessAuthenticationBackend().get_user('edith@example.com')
        self.assertEqual(found_user, desirec_user)

    def test_returns_None_if_no_user_with_that_email(self):
        """
        测试没有获取到用户的邮箱信息时返回None
        """
        self.assertIsNone(PasswordlessAuthenticationBackend().get_user('edith@example.com'))