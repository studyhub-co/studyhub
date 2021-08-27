# Generated by Django 2.2.11 on 2020-04-12 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_auto_20200318_0848'),
    ]

    operations = [
        migrations.AddField(
            model_name='material',
            name='screenshot',
            field=models.ImageField(blank=True, null=True, upload_to='materials_images'),
        ),
        migrations.AlterField(
            model_name='materialproblemtypesandbox',
            name='screenshot_url',
            field=models.ImageField(blank=True, null=True, upload_to='mpt_images'),
        ),
    ]
