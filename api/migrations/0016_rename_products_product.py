# Generated by Django 5.1 on 2024-08-19 03:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_products'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Products',
            new_name='Product',
        ),
    ]
