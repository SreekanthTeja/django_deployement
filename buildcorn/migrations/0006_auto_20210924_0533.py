# Generated by Django 3.2.5 on 2021-09-24 05:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buildcorn', '0005_auto_20210924_0526'),
    ]

    operations = [
        migrations.AlterField(
            model_name='material',
            name='b_qty',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='material',
            name='total_qty',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
