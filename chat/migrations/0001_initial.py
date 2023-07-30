# Generated by Django 3.2.10 on 2022-12-23 21:21

import datetime
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
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500, verbose_name='Чат')),
                ('ad_fk', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='board.board', verbose_name='Объявление №')),
                ('participants', models.ManyToManyField(blank=True, default=None, related_name='participants', to=settings.AUTH_USER_MODEL, verbose_name='Участники чата')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=10000, verbose_name='Сообщение')),
                ('date', models.DateTimeField(blank=True, default=datetime.datetime.now, verbose_name='Дата отправки')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chat.room', verbose_name='Чат №')),
                ('sender', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Отправитель')),
            ],
            options={
                'get_latest_by': 'id',
            },
        ),
    ]
