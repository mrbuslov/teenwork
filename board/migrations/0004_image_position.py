# Generated by Django 3.2.10 on 2022-12-25 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0003_alter_age_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='position',
            field=models.PositiveSmallIntegerField(default=1, verbose_name='Позиция'),
        ),
    ]
