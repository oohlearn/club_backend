# Generated by Django 5.1 on 2024-09-13 03:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('information', '0047_homecontent'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=20, null=True, verbose_name='姓名')),
                ('phone', models.CharField(blank=True, max_length=20, null=True, verbose_name='電話')),
                ('email', models.EmailField(blank=True, max_length=20, null=True, verbose_name='email')),
                ('category', models.CharField(blank=True, max_length=20, null=True, verbose_name='問題種類')),
                ('title', models.CharField(blank=True, max_length=20, null=True, verbose_name='標題')),
                ('content', models.TextField(blank=True, null=True, verbose_name='內容')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='建立日期')),
            ],
        ),
    ]
