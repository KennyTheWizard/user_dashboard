# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-22 14:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20171021_1215'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='description',
            field=models.TextField(blank=True, default=''),
        ),
    ]
