# Generated by Django 5.1 on 2024-08-31 15:06

import tinymce.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopping', '0019_rename_image_index_product_index_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('stationary', '文具'), ('cloth', '服飾（衣服、帽子、襪子）'), ('media', '演出影音')], max_length=500, null=True, verbose_name='商品種類'),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=tinymce.models.HTMLField(blank=True, null=True, verbose_name='商品敘述'),
        ),
        migrations.AlterField(
            model_name='product',
            name='discount_price',
            field=models.IntegerField(blank=True, null=True, verbose_name='特價價格'),
        ),
        migrations.AlterField(
            model_name='product',
            name='state_tag',
            field=models.CharField(blank=True, choices=[('特價中', '特價中'), ('缺貨中', '缺貨中'), ('完售', '完售'), ('新上市', '新上市')], help_text='字樣會顯示在圖片上', max_length=100, null=True, verbose_name='商品標籤'),
        ),
        migrations.AlterField(
            model_name='size',
            name='description',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='備註，例：尺寸描述'),
        ),
        migrations.AlterField(
            model_name='size',
            name='group',
            field=models.CharField(blank=True, choices=[('大人、成年人', '大人、成年人'), ('小孩', '小孩')], max_length=50, null=True, verbose_name='適用族群'),
        ),
    ]
