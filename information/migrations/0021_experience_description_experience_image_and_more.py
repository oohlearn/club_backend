# Generated by Django 5.1 on 2024-08-19 05:25
import tinymce.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('information', '0020_alter_activity_description_alter_album_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='experience',
            name='description',
            field=tinymce.models.HTMLField(blank=True, verbose_name='經歷細節介紹'),
        ),
        migrations.AddField(
            model_name='experience',
            name='image',
            field=models.ImageField(default='Image/None/Noimg.jpg', upload_to='Images/index_stories/', verbose_name='圖片'),
        ),
        migrations.AlterField(
            model_name='experience',
            name='experience',
            field=models.TextField(verbose_name='經歷標題'),
        ),
    ]
