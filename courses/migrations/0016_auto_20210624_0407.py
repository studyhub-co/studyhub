# Generated by Django 2.2.21 on 2021-06-24 08:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0015_auto_20210415_1102'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lessonprogress',
            old_name='score',
            new_name='lesson_progress',
        ),
    ]
