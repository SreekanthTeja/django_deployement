# Generated by Django 3.2.5 on 2021-08-28 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buildcorn', '0004_auto_20210827_1053'),
    ]

    operations = [
        migrations.AlterField(
            model_name='qualitylibrary',
            name='date',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='safetylibrary',
            name='date',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
