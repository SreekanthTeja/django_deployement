# Generated by Django 3.2.5 on 2021-09-22 07:23

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OTP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('otp', models.PositiveIntegerField(blank=True, null=True)),
                ('expiry', models.DateTimeField(blank=True, default=datetime.datetime(2021, 9, 22, 8, 23, 8, 157889, tzinfo=utc), null=True)),
                ('validated', models.BooleanField(blank=True, default=False, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]