# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-07-05 14:04
from __future__ import unicode_literals

from django.db import migrations, models
import django_light_enums.db


class Migration(migrations.Migration):

    dependencies = [
        ('curricula', '0026_auto_20180612_1512'),
    ]

    operations = [
        migrations.AddField(
            model_name='curriculum',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
