# Generated by Django 3.2.10 on 2021-12-24 21:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0003_alter_deletedads_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deletedads',
            name='published',
            field=models.DateTimeField(db_index=True, editable=False, verbose_name='Опубликовано'),
        ),
    ]
