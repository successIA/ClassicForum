# -*- coding: utf-8 -*-
# Generated by Django 1.11.22 on 2019-11-12 02:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('threads', '0002_auto_20191112_0229'),
    ]

    operations = [
        migrations.AlterField(
            model_name='threadactivity',
            name='unread',
            field=models.BooleanField(default=True),
        ),
    ]
