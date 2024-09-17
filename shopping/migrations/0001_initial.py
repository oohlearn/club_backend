# Generated by Django 5.1 on 2024-09-17 05:32

import django.db.models.deletion
import shortuuidfield.fields
import tinymce.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('activity', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', shortuuidfield.fields.ShortUUIDField(blank=True, editable=False, max_length=22, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=10, null=True, verbose_name='訂單總金額')),
                ('shipping_fee', models.DecimalField(decimal_places=2, max_digits=6, null=True, verbose_name='運費')),
                ('discount_amount', models.DecimalField(decimal_places=2, max_digits=10, null=True, verbose_name='折扣金額')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', shortuuidfield.fields.ShortUUIDField(blank=True, editable=False, max_length=22, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=500, verbose_name='商品名稱')),
                ('price', models.IntegerField(verbose_name='原始價格')),
                ('discount_price', models.IntegerField(blank=True, null=True, verbose_name='特價價格')),
                ('category', models.CharField(choices=[('stationary', '文具'), ('cloth', '服飾（衣服、帽子、襪子）'), ('media', '演出影音')], max_length=500, null=True, verbose_name='商品種類')),
                ('quantity', models.IntegerField(blank=True, null=True, verbose_name='庫存總量')),
                ('sold_qty', models.IntegerField(blank=True, null=True, verbose_name='已售出總量')),
                ('pre_sold_qty', models.IntegerField(blank=True, null=True, verbose_name='暫時售出量')),
                ('description', tinymce.models.HTMLField(blank=True, null=True, verbose_name='商品敘述')),
                ('state_tag', models.CharField(blank=True, choices=[('特價中', '特價中'), ('缺貨中', '缺貨中'), ('完售', '完售'), ('新上市', '新上市')], help_text='字樣會顯示在圖片上', max_length=100, null=True, verbose_name='商品標籤')),
                ('on_sell', models.BooleanField(default=True, help_text='若下架該商品，取消勾選', verbose_name='販售中')),
                ('on_discount', models.BooleanField(default=False, help_text='勾選後，顯示特價價格', verbose_name='優惠中')),
                ('index_image', models.ImageField(default='Image/None/Noimg.jpg', upload_to='Images/products/', verbose_name='商品封面照')),
            ],
            options={
                'verbose_name': '商品',
                'verbose_name_plural': '商品列表',
            },
        ),
        migrations.CreateModel(
            name='ProductCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='例：團員優惠', max_length=100, verbose_name='商品折扣碼名稱')),
                ('code', models.CharField(help_text='例：MEMBER', max_length=100, verbose_name='折扣碼')),
                ('discount', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='折扣比例，請直接寫小數，例：0.8')),
                ('is_valid', models.BooleanField(default=False, verbose_name='開啟優惠碼')),
                ('end_date', models.DateField(blank=True, null=True, verbose_name='有效日期')),
                ('description', models.CharField(blank=True, max_length=100, null=True, verbose_name='備註＆說明')),
            ],
            options={
                'verbose_name': '商品優惠碼',
                'verbose_name_plural': '商品優惠碼',
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='姓名')),
                ('email', models.EmailField(max_length=254, verbose_name='電子郵件')),
                ('phone', models.CharField(max_length=20, verbose_name='電話')),
                ('postal_code', models.CharField(max_length=10, verbose_name='郵遞區號')),
                ('address_city', models.CharField(max_length=100, verbose_name='城市')),
                ('address_district', models.CharField(max_length=100, verbose_name='區域')),
                ('address', models.CharField(max_length=1000, verbose_name='詳細地址')),
                ('paid_method', models.CharField(blank=True, choices=[('credit_card', '信用卡'), ('virtual_ATM', 'ATM虛擬帳號'), ('line_pay', 'Line Pay'), ('apple_pay', 'Apple Pay')], max_length=20, verbose_name='付費方式')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='創建時間')),
                ('updated_at', models.DateTimeField(auto_now=True, null=True, verbose_name='更新時間')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '顧客',
                'verbose_name_plural': '顧客',
            },
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('need_deliver_paid', models.BooleanField(default=True, verbose_name='要加運費')),
                ('total_price', models.IntegerField(blank=True, null=True, verbose_name='訂單總金額')),
                ('status', models.CharField(choices=[('unpaid', '未付款'), ('undelivered', '已付款，未出貨'), ('delivered', '已出貨'), ('finished', '已出貨'), ('problem', '問題單'), ('canceled', '已取消')], default='unpaid', max_length=100, verbose_name='訂單狀態')),
                ('deliver_price', models.IntegerField(blank=True, default='70', null=True, verbose_name='運費金額')),
                ('ticket_discount_code', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ticket_discount_code', to='activity.ticketdiscountcode')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shopping.customer', verbose_name='訂購人資料')),
                ('product_code', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='product_code', to='shopping.productcode')),
            ],
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', shortuuidfield.fields.ShortUUIDField(blank=True, editable=False, max_length=22, primary_key=True, serialize=False)),
                ('level', models.CharField(blank=True, max_length=50, verbose_name='顯示順序')),
                ('image_data', models.ImageField(upload_to='Images/albums/', verbose_name='其他商品照片')),
                ('description', models.CharField(blank=True, max_length=255, verbose_name='照片描述')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='shopping.product', verbose_name='商品')),
            ],
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(blank=True, max_length=20, null=True, verbose_name='尺寸或顏色')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cartItem', to='shopping.cart')),
                ('seat', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='activity.seat')),
                ('seat_v2', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='activity.seatfornumberrow')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shopping.product')),
            ],
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(max_length=100, verbose_name='尺寸或顏色')),
                ('group', models.CharField(blank=True, choices=[('大人、成年人', '大人、成年人'), ('小孩', '小孩')], max_length=50, null=True, verbose_name='適用族群')),
                ('description', models.CharField(blank=True, max_length=255, null=True, verbose_name='備註，例：尺寸描述')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='size_list', to='shopping.product', verbose_name='尺寸列表')),
            ],
        ),
    ]
