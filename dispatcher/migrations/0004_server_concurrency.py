# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-06 08:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dispatcher', '0003_auto_20170825_2201'),
    ]

    operations = [
        migrations.AddField(
            model_name='server',
            name='concurrency',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
