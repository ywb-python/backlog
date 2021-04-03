#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/4/1 23:22
# @Author  : ywb
# @Site    : 视图函数的测试
# @File    : test_views.py
# @Software: PyCharm


from django.test import TestCase
from accounts import views
from unittest.mock import patch, call
from accounts.models import Token


class SendLoginEmailViewTest(TestCase):
    """
    视图函数send_login_email的测试
    """

    def test_redirects_to_home_Page(self):
        """
        测试发送登录邮件的url最终会重定向到首页
        """
        response = self.client.post('/accounts/send_login_email', data={
            'email': '18721706546@163.com'
        })
        self.assertRedirects(response, '/')

    # patch装饰器的参数是要打猴子补丁的函数名
    # 将accounts.views.send_mail函数替换为mock_send_email函数
    # 函数执行结束后自动将accounts.views.send_mail函数进行还原
    @patch("accounts.views.send_mail")
    def test_sends_mail_to_address_from_post(self, mock_send_email):
        """
        测试邮件发送的post请求地址
        :param mock_send_email: 补丁函数
        """
        self.client.post('/accounts/send_login_email',
                         data={'email': '18721706546@163.com'})
        self.assertEqual(mock_send_email.called, True)
        # call_args：参数解析，拆解出位置参数和关键字参数
        (subject, body, from_email, to_list), kwargs = mock_send_email.call_args
        self.assertEqual(subject, 'Your login link for Superlists')
        self.assertEqual(from_email, '18721706546@163.com')
        self.assertEqual(to_list, ['18721706546@163.com'])

    def test_adds_success_message(self):
        """
        测试django临时消息
        """
        response = self.client.post('/accounts/send_login_email',
                                    data={'email': '18721706546@163.com'}, follow=True)
        message = list(response.context['messages'])[0]
        self.assertEqual(message.message, "Check your email, we've sent you a link you can use to log in.")
        self.assertEqual(message.tags, 'success')

    def test_creates_token_associated_with_email(self):
        """
        测试数据库中生成的令牌与post请求中的邮件地址是否相关联
        """
        self.client.post('/accounts/send_login_email',
                         data={'email': '18721706546@163.com'})
        token = Token.objects.first()
        self.assertEqual(token.email, '18721706546@163.com')

    @patch("accounts.views.send_mail")
    def test_send_link_to_login_using_toekn_uid(self, mock_send_email):
        """
        测试邮件里的文本是否可以进行登录的token信息
        :param mock_send_email: 补丁函数
        """
        self.client.post('/accounts/send_login_email',
                         data={'email': '18721706546@163.com'})
        token = Token.objects.first()
        excepted_url = f'http://testserver/accounts/login?token={token.uid}'
        (subject, body, from_email, to_list), kwargs = mock_send_email.call_args
        self.assertIn(excepted_url, body)


@patch('accounts.views.auth')
class LoginViewTest(TestCase):
    """
    视图函数login对应的单元测试
    """

    def test_redirects_to_home_page(self, mock_auth):
        """
        测试登录成功之后重定向到首页
        """
        response = self.client.get('/accounts/login?token=abcd123')
        self.assertRedirects(response, '/')

    def test_calls_authenticate_with_uid_from_get_request(self, mock_auth):
        """
        测试通过请求里的uid进行认证
        :param mock_auth: 补丁函数
        """
        self.client.get('/accounts/login?token=abcd123')
        self.assertEqual(mock_auth.authenticate.call_args, call(uid='abcd123'))

    def test_calls_auth_login_with_user_if_there_is_one(self, mock_auth):
        """
        测试authenticate函数是否返回一个用户
        :param mock_auth: 补丁函数
        """
        response = self.client.get('/accounts/login?token=abcd123')
        # return_value:mock_auth.authenticate.return_value即mock_auth.authenticate()
        self.assertEqual(mock_auth.login.call_args, call(response.wsgi_request, mock_auth.authenticate.return_value))

    def test_does_not_login_if_user_is_no_authenticated(self, mock_auth):
        """
        测试未经认证的用户不能登录
        :param mock_auth: 补丁函数
        """
        mock_auth.authenticate.return_value = None
        self.client.get('/accounts/login?token=abcd123')
        self.assertEqual(mock_auth.auth.login.called, False)
