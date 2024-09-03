# Generated by Django 5.1 on 2024-09-03 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0018_seat_is_sold_zone_total_alter_seat_is_chair_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='venue',
            name='size',
            field=models.CharField(choices=[('小型場地', '小型場地（總座位數＜300，座位區塊3塊以內）'), ('中小型場地', '小型場地（總座位數介於300～500，座位區塊6塊以內）'), ('中型場地', '小型場地（總座位數介於500-1200，座位區塊6塊以內）'), ('中大型場地', '小型場地（總座位數介於1200-2000，座位區塊8塊以內）')], default='中小型場地', max_length=100),
        ),
    ]
