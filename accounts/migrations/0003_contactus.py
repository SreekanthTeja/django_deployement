# Generated by Django 3.2.5 on 2021-09-30 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_remove_otp_expiry'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactUs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=30)),
                ('address', models.TextField(blank=True, null=True)),
                ('phone', models.PositiveIntegerField()),
            ],
            options={
                'ordering': ('-id',),
            },
        ),
    ]
