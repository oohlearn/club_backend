# Generated by Django 5.1 on 2024-09-17 08:49

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopping', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ['-created_at'], 'verbose_name': '訂單', 'verbose_name_plural': '訂單列表'},
        ),
        migrations.RenameField(
            model_name='cart',
            old_name='deliver_price',
            new_name='shipping_fee',
        ),
        migrations.RemoveField(
            model_name='order',
            name='discount_amount',
        ),
        migrations.RemoveField(
            model_name='order',
            name='shipping_fee',
        ),
        migrations.AddField(
            model_name='order',
            name='cart',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to='shopping.cart'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='notes',
            field=models.TextField(blank=True, null=True, verbose_name='訂單備註'),
        ),
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('pending', '待處理'), ('processing', '處理中'), ('shipped', '已出貨'), ('delivered', '已送達'), ('cancelled', '已取消'), ('refunded', '已退款')], default='unpaid', max_length=20, verbose_name='訂單狀態'),
        ),
        migrations.AddField(
            model_name='order',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='最後更新時間'),
        ),
        migrations.AlterField(
            model_name='cart',
            name='status',
            field=models.CharField(choices=[('unpaid', '未付款'), ('undelivered', '已付款，未出貨'), ('delivered', '已出貨'), ('delivered', '已送達'), ('finished', '已完成'), ('problem', '問題單'), ('canceled', '已取消'), ('refunded', '已退款')], default='unpaid', max_length=100, verbose_name='訂單狀態'),
        ),
        migrations.AlterField(
            model_name='order',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='創建時間'),
        ),
        migrations.AlterField(
            model_name='order',
            name='total_amount',
            field=models.IntegerField(verbose_name='訂單總金額'),
        ),
    ]
