# Generated by Django 3.2.5 on 2021-09-29 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buildcorn', '0006_banner_multi_images'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='banner',
            name='image',
        ),
        migrations.AlterField(
            model_name='banner',
            name='multi_images',
            field=models.TextField(blank=True, null=True),
        ),
    ]
