# Generated by Django 3.2.5 on 2021-10-04 06:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_contactus_phone'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contactus',
            options={'ordering': ('-id',), 'verbose_name_plural': 'ContactUs'},
        ),
    ]
