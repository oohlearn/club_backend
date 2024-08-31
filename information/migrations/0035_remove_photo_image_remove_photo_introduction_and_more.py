# Generated by Django 5.1 on 2024-08-26 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('information', '0034_conductor_introduction_alter_experience_date_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='photo',
            name='image',
        ),
        migrations.RemoveField(
            model_name='photo',
            name='introduction',
        ),
        migrations.AddField(
            model_name='photo',
            name='albumImage',
            field=models.ImageField(blank=True, upload_to='Images/albums/', verbose_name='照片'),
        ),
    ]
