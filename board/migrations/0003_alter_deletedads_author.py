# Generated by Django 3.2.10 on 2021-12-24 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0002_auto_20211224_0947'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deletedads',
            name='author',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Автор'),
        ),
    ]
