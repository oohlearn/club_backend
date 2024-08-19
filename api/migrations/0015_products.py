# Generated by Django 5.1 on 2024-08-19 03:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_video_tags_alter_album_tags_alter_article_tags'),
    ]

    operations = [
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=500)),
                ('price', models.IntegerField()),
                ('discount_price', models.IntegerField()),
                ('description', models.TextField()),
                ('state_tag', models.CharField(blank=True, max_length=100)),
                ('on_sell', models.BooleanField(default=True)),
                ('image', models.ImageField(default='Image/None/Noimg.jpg', upload_to='Images/teachers/', verbose_name='照片')),
            ],
            options={
                'verbose_name': '商品',
                'verbose_name_plural': '商品列表',
            },
        ),
    ]
