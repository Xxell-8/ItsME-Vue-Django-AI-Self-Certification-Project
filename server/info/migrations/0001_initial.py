# Generated by Django 3.2.7 on 2021-10-01 05:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0006_user_fullname'),
    ]

    operations = [
        migrations.CreateModel(
            name='IdCard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=45)),
                ('birth', models.CharField(blank=True, max_length=8)),
                ('img', models.ImageField(null=True, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.CharField(max_length=45, unique=True)),
                ('name', models.CharField(max_length=45)),
                ('repeatable', models.BooleanField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('expired_at', models.DateTimeField()),
                ('managers', models.ManyToManyField(related_name='links', to=settings.AUTH_USER_MODEL)),
                ('partner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='links', to='accounts.partner')),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_completed', models.BooleanField(default=False)),
                ('completed_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=45)),
                ('birth', models.CharField(max_length=8)),
                ('img', models.ImageField(null=True, upload_to='')),
                ('link', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customers', to='info.link')),
            ],
        ),
    ]
