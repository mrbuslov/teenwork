# Generated by Django 3.2.10 on 2022-12-24 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0002_auto_20221224_0859'),
    ]

    operations = [
        migrations.AlterField(
            model_name='age',
            name='name',
            field=models.PositiveIntegerField(db_index=True, verbose_name='Возраст'),
        ),
    ]
