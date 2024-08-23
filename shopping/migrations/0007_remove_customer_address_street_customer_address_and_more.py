# Generated by Django 5.1 on 2024-08-23 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopping', '0006_remove_orderitem_tickets_remove_productcart_products_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='address_street',
        ),
        migrations.AddField(
            model_name='customer',
            name='address',
            field=models.CharField(default='default', max_length=1000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customer',
            name='paid_method',
            field=models.CharField(blank=True, choices=[('credit_card', '信用卡'), ('virtual_ATM', 'ATM虛擬帳號')], max_length=100, verbose_name='付費方式'),
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.CharField(default='default', max_length=500, verbose_name='商品種類'),
            preserve_default=False,
        ),
    ]
