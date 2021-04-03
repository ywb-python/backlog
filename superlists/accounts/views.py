from django.shortcuts import redirect
from django.core.mail import send_mail
from django.contrib import auth, messages
from accounts.models import Token
from django.urls import reverse
import sys


def send_login_email(request):
    """
    send_login_email对应的视图函数,
    """
    email = request.POST['email']
    token = Token.objects.create(email=email)
    # build_absolute_uri():Django构建完整url的一种方式
    url = request.build_absolute_uri(reverse('login') + '?token=' + str(token.uid))
    message_body = f'Use this link to log in:\n\n{url}'
    send_mail('Your login link for Superlists', message_body, '18721706546@163.com', [email])
    messages.success(request, "Check your email, we've sent you a link you can use to log in.")
    return redirect('/')


def login(request):
    """
    login对应的视图函数
    """
    user = auth.authenticate(uid=request.GET.get('token'))
    if user:
        auth.login(request, user)
    return redirect('/')

# Create your views here.
