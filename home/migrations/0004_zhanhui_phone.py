# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-04 16:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_auto_20180104_1654'),
    ]

    operations = [
        migrations.AddField(
            model_name='zhanhui',
            name='phone',
            field=models.IntegerField(blank=True, null=True, verbose_name='电话'),
        ),
    ]
