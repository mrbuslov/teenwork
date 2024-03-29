# Generated by Django 3.2.10 on 2022-12-24 08:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='board',
            name='age_to',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='age_to', to='board.age', verbose_name='Возраст до'),
        ),
        migrations.AddField(
            model_name='deletedads',
            name='age_to',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='age_to_deleted', to='board.age', verbose_name='Возраст до'),
        ),
        migrations.AlterField(
            model_name='board',
            name='age',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='age', to='board.age', verbose_name='Возраст'),
        ),
        migrations.AlterField(
            model_name='deletedads',
            name='age',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='age_deleted', to='board.age', verbose_name='Возраст от'),
        ),
    ]
