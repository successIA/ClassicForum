# -*- coding: utf-8 -*-
# Generated by Django 1.11.22 on 2019-11-13 16:38
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('threads', '0005_thread_followers2'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='threadfollowership',
            name='final_comment',
        ),
        migrations.RemoveField(
            model_name='threadfollowership',
            name='thread',
        ),
        migrations.RemoveField(
            model_name='threadfollowership',
            name='user',
        ),
        migrations.RemoveField(
            model_name='thread',
            name='followers',
        ),
        migrations.DeleteModel(
            name='ThreadFollowership',
        ),
    ]