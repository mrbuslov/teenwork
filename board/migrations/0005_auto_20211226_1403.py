# Generated by Django 3.2.10 on 2021-12-26 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0004_alter_deletedads_published'),
    ]

    operations = [
        migrations.AlterField(
            model_name='city',
            name='name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='city',
            name='name_ru',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='city',
            name='name_uk',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
