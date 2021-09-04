# Generated by Django 3.2.5 on 2021-09-03 15:01

import accounts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='no_licenses',
        ),
        migrations.AddField(
            model_name='company',
            name='company_id',
            field=models.CharField(default=accounts.models.uniqueid, max_length=30),
        ),
        migrations.AlterField(
            model_name='user',
            name='client_id',
            field=models.UUIDField(default=219382791538736),
        ),
    ]
