# Generated by Django 3.2.10 on 2022-12-23 21:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('board', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Telegram',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telegram', models.BooleanField(default=False, null=True, verbose_name='Telegram')),
                ('region', models.CharField(blank=True, max_length=100, null=True, verbose_name='Область')),
                ('city', models.CharField(blank=True, max_length=100, null=True, verbose_name='Город')),
                ('chat_id', models.BigIntegerField(blank=True, editable=False, null=True, verbose_name='chat id')),
                ('age', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='board.age', verbose_name='Возраст')),
                ('person', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Человек')),
                ('rubric', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='board.rubric', verbose_name='Рубрика')),
            ],
            options={
                'verbose_name': 'Telegram',
                'verbose_name_plural': 'Telegram Users',
                'ordering': ['telegram'],
            },
        ),
    ]
