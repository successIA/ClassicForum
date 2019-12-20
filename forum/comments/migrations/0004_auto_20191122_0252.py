# -*- coding: utf-8 -*-
# Generated by Django 1.11.22 on 2019-11-22 01:52
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0003_comment_offset'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='downvoters',
            field=models.ManyToManyField(blank=True, related_name='downvoted_comments', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='comment',
            name='upvoters',
            field=models.ManyToManyField(blank=True, related_name='upvoted_comments', to=settings.AUTH_USER_MODEL),
        ),
    ]