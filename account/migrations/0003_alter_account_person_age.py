# Generated by Django 3.2.10 on 2021-12-12 21:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0001_initial'),
        ('account', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='person_age',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='board.age', verbose_name='Возраст'),
        ),
    ]
