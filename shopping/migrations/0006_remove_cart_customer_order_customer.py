# Generated by Django 5.1 on 2024-09-23 03:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopping', '0005_alter_cartitem_product'),
        ('user', '0008_userprofile_customer_user_profile_delete_customuser'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='customer',
        ),
        migrations.AddField(
            model_name='order',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='user.customer', verbose_name='訂購人資料'),
        ),
    ]
