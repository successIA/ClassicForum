# -*- coding: utf-8 -*-
# Generated by Django 1.11.22 on 2020-01-01 17:06
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('moderation', '0004_auto_20200101_1738'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='moderatorevent',
            name='hidden_by',
        ),
        migrations.RemoveField(
            model_name='moderatorevent',
            name='unhidden_by',
        ),
    ]