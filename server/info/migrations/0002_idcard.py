# Generated by Django 3.2.7 on 2021-09-30 02:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='IdCard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
                ('birth', models.CharField(max_length=8)),
                ('img', models.ImageField(upload_to='')),
            ],
        ),
    ]
