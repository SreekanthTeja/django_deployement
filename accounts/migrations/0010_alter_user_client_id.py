# Generated by Django 3.2.5 on 2021-09-03 06:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_alter_user_client_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='client_id',
            field=models.UUIDField(default=254543722241769),
        ),
    ]
