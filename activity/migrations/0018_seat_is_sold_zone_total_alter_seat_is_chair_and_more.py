# Generated by Django 5.1 on 2024-09-03 13:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0017_seat_is_chair_alter_venue_map_url_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='seat',
            name='is_sold',
            field=models.BooleanField(default=False, verbose_name='已售出'),
        ),
        migrations.AddField(
            model_name='zone',
            name='total',
            field=models.IntegerField(blank=True, null=True, verbose_name='總數'),
        ),
        migrations.AlterField(
            model_name='seat',
            name='is_chair',
            field=models.BooleanField(default=False, verbose_name='輪椅席'),
        ),
        migrations.AlterField(
            model_name='seat',
            name='seat_num',
            field=models.CharField(max_length=10, verbose_name='座位號碼'),
        ),
        migrations.AlterField(
            model_name='seat',
            name='zone',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seat', to='activity.zone', verbose_name='區域'),
        ),
        migrations.AlterField(
            model_name='zone',
            name='area',
            field=models.CharField(blank=True, choices=[('前左', '前左'), ('前中', '前中'), ('前右', '前右'), ('中左', '中左'), ('中中', '中中'), ('中右', '中右'), ('後左', '後左'), ('後中', '後中'), ('後右', '後右')], help_text='例：普通票A區、普通票B區', max_length=50, null=True, verbose_name='區域相對位置'),
        ),
    ]
