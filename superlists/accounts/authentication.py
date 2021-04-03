#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/4/3 15:59
# @Author  : ywb
# @Site    : 用户身份验证
# @File    : authentication.py
# @Software: PyCharm


import sys
from accounts.models import User, Token


class PasswordlessAuthenticationBackend(object):
    """
    密码验证
    """

    def authenticate(self, uid):
        """
        用户身份验证
        :param uid: 用户uid
        """
        try:
            token = Token.objects.get(uid=uid)
            return User.objects.get(email=token.email)
        except User.DoesNotExist:
            return User.objects.create(email=token.email)
        except Token.DoesNotExist:
            return None

    def get_user(self, email):
        """
        获取用户信息
        :param email: 邮件地址
        """
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None
