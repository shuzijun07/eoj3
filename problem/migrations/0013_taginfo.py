# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2018-01-12 17:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tagging', '0002_on_delete'),
        ('problem', '0012_auto_20180107_1224'),
    ]

    operations = [
        migrations.CreateModel(
            name='TagInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True)),
                ('tag', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='tagging.Tag')),
            ],
        ),
    ]
