from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Partner(models.Model):
    code = models.IntegerField()
    name = models.CharField(max_length=45)


class User(AbstractUser):
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE)
    auth = models.IntegerField(default=0)   # 0: 실무자, 1: 관리자