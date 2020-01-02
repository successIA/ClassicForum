# -*- coding: utf-8 -*-
# Generated by Django 1.11.22 on 2020-01-02 19:01
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('threads', '0012_auto_20191124_0435'),
    ]

    operations = [
        migrations.AddField(
            model_name='thread',
            name='hidden_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
    ]