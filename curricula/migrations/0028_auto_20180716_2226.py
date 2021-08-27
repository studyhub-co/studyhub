# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-07-17 02:26
from __future__ import unicode_literals

from django.db import migrations
import django_light_enums.db
# import jsonfield.fields
import django.contrib.postgres.fields


class Migration(migrations.Migration):

    dependencies = [
        ('curricula', '0027_auto_20180705_1704'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='lesson_type',
            field=django_light_enums.db.EnumField(choices=[(0, 'DEFAULT'), (1, 'GAME')], default=0, enum_values=(0, 1)),
        ),
        migrations.AlterField(
            model_name='lessonprogress',
            name='status',
            field=django_light_enums.db.EnumField(choices=[(0, 'LOCKED'), (10, 'NEW'), (20, 'UNLOCKED'), (30, 'COMPLETE')], default=0, enum_values=(0, 10, 20, 30)),
        ),
        migrations.AlterField(
            model_name='question',
            name='answer_type',
            field=django_light_enums.db.EnumField(choices=[(0, 'UNDEFINED'), (100, 'MULTIPLE_CHOICE'), (110, 'MULTISELECT_CHOICE'), (20, 'VECTOR'), (30, 'NULLABLE_VECTOR'), (50, 'MATHEMATICAL_EXPRESSION'), (60, 'VECTOR_COMPONENTS'), (70, 'UNIT_CONVERSION')], default=0, enum_values=(0, 100, 110, 20, 30, 50, 60, 70)),
        ),
        migrations.AlterField(
            model_name='unitconversion',
            name='conversion_steps',
            # field=jsonfield.fields.JSONField(blank=True, default=[{'denominator': '', 'numerator': ''}], help_text='Numerator/Denominator steps', null=True),
            field=django.contrib.postgres.fields.JSONField(blank=True, default=[{'denominator': '', 'numerator': ''}], help_text='Numerator/Denominator steps', null=True),
        ),
    ]
