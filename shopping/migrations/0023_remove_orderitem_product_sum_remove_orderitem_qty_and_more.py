# Generated by Django 5.1 on 2024-09-10 03:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0040_alter_discountcode_discount'),
        ('shopping', '0022_productcode_orderitem_discount_code_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='product_sum',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='qty',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='tickets',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='ticketsV2',
        ),
        migrations.AddField(
            model_name='orderitem',
            name='quantity',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='seat',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='activity.seat'),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='seat_v2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='activity.seatfornumberrow'),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='subtotal',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='discount_code',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='activity.discountcode'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='shopping.order'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shopping.product'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='product_code',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='shopping.productcode'),
        ),
        migrations.AlterField(
            model_name='productcode',
            name='discount',
            field=models.DecimalField(decimal_places=2, max_digits=5, verbose_name='折扣比例，請直接寫小數，例：0.8'),
        ),
    ]
