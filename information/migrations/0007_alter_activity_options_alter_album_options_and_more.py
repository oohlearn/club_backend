# Generated by Django 5.1 on 2024-08-17 03:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('information', '0006_rename_albums_album'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='activity',
            options={'verbose_name': '活動', 'verbose_name_plural': '活動列表'},
        ),
        migrations.AlterModelOptions(
            name='album',
            options={'verbose_name': '相簿', 'verbose_name_plural': '相簿列表'},
        ),
        migrations.AlterModelOptions(
            name='article',
            options={'verbose_name': '文章', 'verbose_name_plural': '文章列表'},
        ),
        migrations.AlterModelOptions(
            name='experience',
            options={'verbose_name': '經歷', 'verbose_name_plural': '經歷列表'},
        ),
        migrations.AlterModelOptions(
            name='indexstory',
            options={'verbose_name': '封面故事', 'verbose_name_plural': '封面故事列表'},
        ),
        migrations.AlterModelOptions(
            name='teacher',
            options={'verbose_name': '老師', 'verbose_name_plural': '老師列表'},
        ),
        migrations.AlterModelOptions(
            name='video',
            options={'verbose_name': '影片', 'verbose_name_plural': '影片列表'},
        ),
        migrations.AddField(
            model_name='indexstory',
            name='btn_text',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='indexstory',
            name='description',
            field=models.TextField(default='default'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='activity',
            name='description',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='description',
            field=models.TextField(blank=True),
        ),
    ]
