from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser  # AbstractBaseUser仅包含身份验证功能
from django.contrib.auth.base_user import BaseUserManager  # 可以生成随机密码
from django.contrib.auth.hashers import make_password  # 密码加密

from .base import BaseModel, BaseManager


class UserManager(BaseUserManager, BaseManager):
    pass


class User(BaseModel, AbstractBaseUser):
    # ROLE_CHOICES = [
    #
    # ]
    user_name = models.CharField(db_index=True, null=False, blank=False, max_length=255, verbose_name='用户名')
    password = models.CharField(max_length=128, null=False, blank=True, verbose_name='password')
    phone = models.CharField(db_index=True, max_length=11, default=None, verbose_name='手机号')
    email = models.CharField(db_index=True, max_length=20, default=None, verbose_name='邮箱')
    role = models.CharField(
        db_index=True, null=False, blank=False, max_length=28, verbose_name='用户角色'
    )

    objects = UserManager()  # 身份验证 + 随机密码
    USERNAME_FIELD = "id"  # 描述User模型上用作唯一标识符的字段名称的字符串

    def __str__(self, ):
        return f"User: <id: {self.id} user_name: {self.user_name}>"

    def __repr__(self, ):
        return str(self)

    @classmethod
    def create_user(cls, user_name, password, role, email=None, phone=None):
        if role == "admin":
            phone = None,
            email = None,

        user = cls(
            user_name=user_name, password=make_password(password),
            role=role, email=email, phone=phone
        )
        user.save()
        return user

    @classmethod
    def create_admin(cls, user_name, password):
        return cls.create_user(user_name=user_name, password=password, role="admin")
