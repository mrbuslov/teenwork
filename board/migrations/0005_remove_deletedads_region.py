# Generated by Django 3.2.10 on 2022-12-26 08:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0004_image_position'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deletedads',
            name='region',
        ),
    ]
