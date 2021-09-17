from django.db import models
from accounts.models import Partner
from django.contrib.auth import get_user_model

# Create your models here.
class Template(models.Model):
    name = models.CharField(max_length=45)
    logo = models.ImageField()
    content = models.TextField(blank=True)
    motion = models.BooleanField()
    id_name = models.BooleanField()
    id_code = models.BooleanField()
    id_date = models.BooleanField()
    id_img = models.BooleanField()


class Link(models.Model):
    name = models.CharField(max_length=45)
    repeatable = models.BooleanField()
    created_date = models.DateTimeField(auto_now_add=True)
    expriation_date = models.DateTimeField()
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE)
    template = models.ForeignKey(Template, on_delete=models.CASCADE)
    manage_users = models.ManyToManyField(get_user_model(), related_name='manage_links')


class Customer(models.Model):
    link = models.ForeignKey(Link, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    completed_time = models.DateTimeField(null=True)
    name = models.CharField(max_length=45)
    img = models.ImageField(null=True)
    code = models.CharField(max_length=45, null=True)
    date = models.DateField(null=True)