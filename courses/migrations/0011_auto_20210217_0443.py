# Generated by Django 2.2.15 on 2021-02-17 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0010_auto_20210129_0300'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userreaction',
            name='reacted_on',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='userreaction',
            name='reaction_start_on',
            field=models.DateTimeField(),
        ),
    ]
