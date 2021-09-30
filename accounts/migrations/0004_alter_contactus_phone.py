# Generated by Django 3.2.5 on 2021-09-30 10:16

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_contactus'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactus',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None),
        ),
    ]
