# Generated by Django 5.0.6 on 2024-11-05 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='cover_image',
            field=models.ImageField(blank=True, null=True, upload_to='album_covers/'),
        ),
    ]
