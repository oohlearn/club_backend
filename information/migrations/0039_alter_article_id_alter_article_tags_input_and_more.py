# Generated by Django 5.1 on 2024-08-30 04:21

import shortuuidfield.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('information', '0038_alter_album_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='id',
            field=shortuuidfield.fields.ShortUUIDField(blank=True, editable=False, max_length=22, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='article',
            name='tags_input',
            field=models.CharField(blank=True, max_length=300, verbose_name='Hashtag 標記'),
        ),
        migrations.AlterField(
            model_name='introduction',
            name='id',
            field=shortuuidfield.fields.ShortUUIDField(blank=True, editable=False, max_length=22, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='photo',
            name='id',
            field=shortuuidfield.fields.ShortUUIDField(blank=True, editable=False, max_length=22, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(help_text='請用『半形逗號』分開，例：甲, 乙, 丙', max_length=100),
        ),
        migrations.AlterField(
            model_name='video',
            name='id',
            field=shortuuidfield.fields.ShortUUIDField(blank=True, editable=False, max_length=22, primary_key=True, serialize=False),
        ),
    ]
