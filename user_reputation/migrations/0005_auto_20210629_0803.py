# Generated by Django 2.2.21 on 2021-06-29 12:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_reputation', '0004_remove_reputationaction_old_object_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reputationaction',
            old_name='new_object_id',
            new_name='object_id',
        ),
    ]
