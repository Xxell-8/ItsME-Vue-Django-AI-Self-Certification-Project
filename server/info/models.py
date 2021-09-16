from django.db import models
from accounts.models import Partner, User

# Create your models here.
class Template(models.Model):
    name = models.CharField(max_length=45)
    logo = models.ImageField()
    content = models.TextField()
    motion = models.BooleanField()
    id_name = models.BooleanField()
    id_code = models.BooleanField()
    id_date = models.BooleanField()
    id_img = models.BooleanField()


class Link(models.Model):
    name = models.CharField(max_length=45)
    repeatable = models.BooleanField()
    create_date = models.DateTimeField(auto_now_add=True)
    expriation_date = models.DateTimeField()
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE)
    template = models.ForeignKey(Template, on_delete=models.CASCADE)
    manage_users = models.ManyToManyField(User, related_name='manage_links')


class Customer(models.Model):
    link = models.ForeignKey(Link, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    completed_time = models.DateTimeField(blank=True)
    name = models.CharField(max_length=45)
    img = models.ImageField(blank=True)
    code = models.CharField(max_length=45, blank=True)
    date = models.DateField(blank=True)