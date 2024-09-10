# Generated by Django 5.1 on 2024-09-10 03:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0040_alter_discountcode_discount'),
        ('shopping', '0023_remove_orderitem_product_sum_remove_orderitem_qty_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='discount_code',
        ),
        migrations.AddField(
            model_name='order',
            name='discount_code',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='activity.discountcode'),
        ),
        migrations.AlterField(
            model_name='order',
            name='total_price',
            field=models.IntegerField(blank=True, null=True, verbose_name='訂單總金額'),
        ),
    ]
