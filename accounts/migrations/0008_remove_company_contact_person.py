# Generated by Django 3.2.5 on 2021-09-14 09:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_auto_20210908_1642'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='contact_person',
        ),
    ]
