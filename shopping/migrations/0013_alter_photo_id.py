# Generated by Django 5.1 on 2024-08-24 09:12

import shortuuidfield.fields
import uuid
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shopping', '0012_remove_product_image_2_remove_product_image_3_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='id',
            field=shortuuidfield.fields.ShortUUIDField(blank=True, default=uuid.uuid4, editable=False, max_length=22, primary_key=True, serialize=False),
        ),
    ]
