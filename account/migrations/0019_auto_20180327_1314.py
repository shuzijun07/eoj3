# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-03-27 13:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0018_school'),
    ]

    operations = [
        migrations.AddField(
            model_name='school',
            name='abbr',
            field=models.CharField(default='E', max_length=192, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='school',
            name='alias',
            field=models.CharField(blank=True, max_length=192),
        ),
    ]
