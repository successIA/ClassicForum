# -*- coding: utf-8 -*-
# Generated by Django 1.11.28 on 2020-02-19 18:00
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('threads', '0014_remove_thread_hidden_by'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='threadfollowership',
            options={'verbose_name': 'Thread Followership'},
        ),
        migrations.AlterModelOptions(
            name='threadrevision',
            options={'verbose_name': 'Thread Revision'},
        ),
    ]
