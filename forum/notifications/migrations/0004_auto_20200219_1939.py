# -*- coding: utf-8 -*-
# Generated by Django 1.11.28 on 2020-02-19 18:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0003_auto_20200219_1900'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='notif_type',
            field=models.CharField(choices=[('th_crd', 'created'), ('th_upd', 'updated'), ('co_crd', 'commented'), ('co_lik', 'liked'), ('co_rep', 'posted a reply'), ('us_men', 'mentioned'), ('us_fld', 'following')], max_length=6),
        ),
    ]
