# Generated by Django 3.2.7 on 2021-09-16 08:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Template',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
                ('logo', models.ImageField(upload_to='')),
                ('content', models.TextField()),
                ('motion', models.BooleanField()),
                ('id_name', models.BooleanField()),
                ('id_code', models.BooleanField()),
                ('id_date', models.BooleanField()),
                ('id_img', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
                ('repeatable', models.BooleanField()),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('expriation_date', models.DateTimeField()),
                ('manage_users', models.ManyToManyField(related_name='manage_links', to=settings.AUTH_USER_MODEL)),
                ('partner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.partner')),
                ('template', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='info.template')),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_completed', models.BooleanField(default=False)),
                ('completed_time', models.DateTimeField(blank=True)),
                ('name', models.CharField(max_length=45)),
                ('img', models.ImageField(blank=True, upload_to='')),
                ('code', models.CharField(blank=True, max_length=45)),
                ('date', models.DateField(blank=True)),
                ('link', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='info.link')),
            ],
        ),
    ]
