from django.db import models
from accounts.models import Partner
from django.contrib.auth import get_user_model

# Create your models here.
class Link(models.Model):
    path = models.CharField(max_length=45, unique=True)
    name = models.CharField(max_length=45)
    repeatable = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    expired_at = models.DateTimeField()
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, related_name='links')
    managers = models.ManyToManyField(get_user_model(), related_name='links')


class Customer(models.Model):
    link = models.ForeignKey(Link, on_delete=models.CASCADE, related_name='customers')
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=45)
    birth = models.CharField(max_length=8)
    img = models.ImageField(null=True)


class IdCard(models.Model):
    name = models.CharField(max_length=45, blank=True)
    birth = models.CharField(max_length=8, blank=True)
    img = models.ImageField(null=True)