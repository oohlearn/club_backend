# Generated by Django 5.1 on 2024-08-31 15:06

import tinymce.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('information', '0039_alter_article_id_alter_article_tags_input_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='description',
            field=tinymce.models.HTMLField(blank=True, null=True, verbose_name='相簿介紹'),
        ),
        migrations.AlterField(
            model_name='article',
            name='content',
            field=tinymce.models.HTMLField(verbose_name='文章內容'),
        ),
        migrations.AlterField(
            model_name='article',
            name='tags_input',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='Hashtag 標記'),
        ),
        migrations.AlterField(
            model_name='conductor',
            name='description',
            field=tinymce.models.HTMLField(blank=True, null=True, verbose_name='指揮簡介'),
        ),
        migrations.AlterField(
            model_name='conductor',
            name='experiences',
            field=tinymce.models.HTMLField(blank=True, null=True, verbose_name='指揮經歷'),
        ),
        migrations.AlterField(
            model_name='experience',
            name='description',
            field=tinymce.models.HTMLField(blank=True, null=True, verbose_name='經歷細節介紹'),
        ),
        migrations.AlterField(
            model_name='indexstory',
            name='btn_text',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='indexstory',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='描述（不超過10個字）'),
        ),
        migrations.AlterField(
            model_name='indexstory',
            name='place',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='場地'),
        ),
        migrations.AlterField(
            model_name='indexstory',
            name='url',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='introduction',
            name='description',
            field=tinymce.models.HTMLField(blank=True, null=True, verbose_name='介紹內容'),
        ),
        migrations.AlterField(
            model_name='photo',
            name='description',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='照片描述'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='group',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='組別'),
        ),
        migrations.AlterField(
            model_name='video',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='演出內容敘述'),
        ),
        migrations.AlterField(
            model_name='video',
            name='embed_url',
            field=models.CharField(blank=True, max_length=1000, null=True, verbose_name='youtube內嵌網址(請點選youtube分享)'),
        ),
    ]
