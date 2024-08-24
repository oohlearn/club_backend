# Generated by Django 5.1 on 2024-08-24 08:28

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopping', '0010_rename_total_cartitem_sum_cart_deliver_paid_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('image_data', models.ImageField(upload_to='Images/albums/', verbose_name='照片')),
                ('description', models.CharField(blank=True, max_length=255, verbose_name='照片描述')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='shopping.product', verbose_name='商品')),
            ],
        ),
    ]
