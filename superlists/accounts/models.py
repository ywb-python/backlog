from django.db import models
import uuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib import auth


auth.signals.user_logged_in.disconnect(auth.models.update_last_login)


class User(models.Model):
    email = models.EmailField(primary_key=True)
    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'
    is_anonymous = False
    is_authenticated = True


class Token(models.Model):
    email = models.EmailField()
    uid = models.CharField(default=uuid.uuid4, max_length=40)


class ListUserManager(BaseUserManager):
    """
    ListUser模型管理器
    """

    def create_user(self, email):
        """
        产生用户
        :param email: 邮件地址
        """
        ListUser.objects.create(email=email)

    def create_superuser(self, email, password):
        """
        产生超级用户
        :param email: 邮件地址
        :param password: 密码
        """
        self.create_user(email)


class ListUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(primary_key=True)
    USERNAME_FIELD = 'email'
    objects = ListUserManager()

    @property
    def is_staff(self):
        return self.email == '18721706546@163.com'

    @property
    def is_active(self):
        return True

# Create your models here.
