# Generated by Django 3.2.7 on 2021-09-24 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20210924_1729'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partner',
            name='code',
            field=models.CharField(max_length=45, null=True),
        ),
        migrations.AlterField(
            model_name='partner',
            name='name',
            field=models.CharField(max_length=45, null=True),
        ),
    ]
