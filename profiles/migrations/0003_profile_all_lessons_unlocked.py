# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-07 04:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_profile_sound_enabled'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='all_lessons_unlocked',
            field=models.BooleanField(default=False),
        ),
    ]
