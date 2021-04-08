#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/4/5 11:05
# @Author  : ywb
# @Site    : 产生会话
# @File    : create_session.py
# @Software: PyCharm


from django.conf import settings
from django.contrib.auth import BACKEND_SESSION_KEY, SESSION_KEY, get_user_model
from django.contrib.sessions.backends.db import SessionStore
from django.core.management.base import BaseCommand


User = get_user_model()


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_arguments('email')

    def handle(self, *args, **options):
        session_key = create_pre_authenticated_session(options['email'])
        self.stdout.write(session_key)


def create_pre_authenticated_session(email):
    user = User.objects.create(email=email)
    session = SessionStore()
    session[SESSION_KEY] = user.pk
    session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
    session.save()
    return session.session_key

