# Generated by Django 5.1 on 2024-09-17 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopping', '0002_alter_order_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='total_amount',
            field=models.IntegerField(blank=True, null=True, verbose_name='訂單總金額'),
        ),
    ]
