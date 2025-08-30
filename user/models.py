from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class myUser(AbstractBaseUser):
    user_id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class UserToken(models.Model):
    token_id = models.AutoField(primary_key=True)
    email = models.EmailField()
    token = models.CharField(max_length=255)  # 存储验证码或临时令牌
    token_type = models.CharField(max_length=50)  # 验证码类型（如 'email_verification'、'password_reset'）
    created_at = models.DateTimeField(auto_now_add=True)  # 记录创建时间
    updated_at = models.DateTimeField(auto_now=True)  # 记录更新时间
    expires_at = models.DateTimeField()  # 验证码过期时间

    class Meta:
        # 每个用户同一类型的 token 唯一
        unique_together = ('email', 'token_type')

    def is_expired(self):
        """检查 token 是否过期"""
        return self.expires_at < timezone.now()

    def __str__(self):
        return f"Token for {self.email} - {self.token} ({self.token_type})"
