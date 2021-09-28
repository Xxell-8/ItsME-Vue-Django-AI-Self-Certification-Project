from django.core.validators import MaxLengthValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class Partner(models.Model):
    code = models.CharField(max_length=45, null=True)
    name = models.CharField(max_length=45, null=True)


class User(AbstractUser):
    partner = models.ForeignKey(Partner, related_name='users', on_delete=models.CASCADE, null=True)
    username = None
    # name 은 기업명
    name = models.CharField(max_length=45, null=True)
    fullname = models.CharField(max_length=45, null=True)
    code = models.CharField(max_length=45, null=True)
    email = models.EmailField(_('email address'), unique=True)
    phone = models.CharField(max_length=45, null=True)
    auth = models.IntegerField(default=0)   # 0: 실무자, 1: 관리자
    approval = models.IntegerField(default=0) # 0: 가입 대기중, 1: 가입 승인됨

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email