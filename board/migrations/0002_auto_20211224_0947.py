# Generated by Django 3.2.10 on 2021-12-24 09:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('board', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='deletedads',
            name='workers',
            field=models.ManyToManyField(blank=True, default=None, related_name='deleted_adt_workers', to=settings.AUTH_USER_MODEL, verbose_name='Принятые на работу'),
        ),
        migrations.AlterField(
            model_name='deletedads',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='deleted_adt_author', to=settings.AUTH_USER_MODEL, verbose_name='Автор'),
        ),
    ]
