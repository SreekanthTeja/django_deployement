# Generated by Django 3.2.5 on 2021-09-17 07:59

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_otp'),
    ]

    operations = [
        migrations.AddField(
            model_name='otp',
            name='validated',
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
        migrations.AlterField(
            model_name='otp',
            name='expiry',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 9, 17, 8, 59, 27, 411472, tzinfo=utc), null=True),
        ),
    ]