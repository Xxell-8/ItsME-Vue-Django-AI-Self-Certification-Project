# Generated by Django 3.2.7 on 2021-09-23 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20210923_1617'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partner',
            name='phone',
            field=models.CharField(max_length=45, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(max_length=45, null=True),
        ),
    ]
