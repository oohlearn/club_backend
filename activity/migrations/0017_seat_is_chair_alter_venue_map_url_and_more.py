# Generated by Django 5.1 on 2024-09-03 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0016_zone_area_alter_zone_color_alter_zone_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='seat',
            name='is_chair',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='venue',
            name='map_url',
            field=models.CharField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='venue',
            name='total_seats',
            field=models.IntegerField(blank=True),
        ),
    ]
