#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/4/5 11:18
# @Author  : ywb
# @Site    : 
# @File    : server_tools.py
# @Software: PyCharm


from fabric.api import run
from fabric.context_managers import settings


def _get_manage_dot_pay(host):
    return f'~/sites/{host}/virtualenv/bin/python ~/site/{host}/source/manage.py'


def create_database(host):
    manage_dot_py = _get_manage_dot_pay(host)
    with settings(host_string=f'elspeth@{host}'):
        run(f'{manage_dot_py} flush --noinput')


def create_session_on_server(host, email):
    manage_dot_pay = _get_manage_dot_pay(host)
    with settings(host_string=f'elspeth@{host}'):
        session_key = run(f'{manage_dot_pay} create_session {email}')
        return session_key.strip()