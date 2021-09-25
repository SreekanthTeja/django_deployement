# Generated by Django 3.2.5 on 2021-09-25 05:08

import accounts.models
import datetime
from django.conf import settings
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc
import django.utils.timezone
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('user_type', models.CharField(choices=[('SA', 'SuperAdmin'), ('TN', 'Tenent'), ('NU', 'NU')], default='NU', max_length=5)),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='Email Address')),
                ('client_id', models.CharField(blank=True, default=accounts.models.uniqueid, max_length=70, null=True)),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, unique=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('license_count', models.PositiveIntegerField()),
                ('features', models.TextField(blank=True, null=True, verbose_name='Features')),
                ('amount', models.FloatField()),
            ],
            options={
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_id', models.CharField(blank=True, max_length=200, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('payment_mode', models.CharField(choices=[('IBNK', 'Internet Banking'), ('MBNK', 'Mobile Banking'), ('EWLT', 'Wallet'), ('DEBT', 'Debit card'), ('CRDT', 'Credit card'), ('UPI', 'UPI'), ('CASH', 'Cash'), ('CHEK', 'Check')], max_length=4)),
                ('status', models.PositiveSmallIntegerField(blank=True, choices=[(1, 'Done'), (2, 'Pending'), (3, 'Failed')], null=True)),
                ('amount', models.FloatField(blank=True, null=True)),
                ('due_amount', models.FloatField(blank=True, null=True)),
                ('pickup_type', models.CharField(choices=[('ONL', 'Online'), ('OFL', 'Offline')], max_length=3)),
                ('response', models.TextField(blank=True, max_length=1000, null=True)),
                ('company_name', models.CharField(blank=True, max_length=50, null=True)),
                ('holder', models.TextField(blank=True, null=True)),
                ('plan', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='plan_payments', to='accounts.plan')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Payment',
                'verbose_name_plural': 'Payments',
            },
        ),
        migrations.CreateModel(
            name='OTP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('otp', models.PositiveIntegerField(blank=True, null=True)),
                ('expiry', models.DateTimeField(blank=True, default=datetime.datetime(2021, 9, 25, 6, 8, 13, 648675, tzinfo=utc), null=True)),
                ('validated', models.BooleanField(blank=True, default=False, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('company_id', models.CharField(default=accounts.models.uniqueid, max_length=50)),
                ('gstin', models.CharField(blank=True, max_length=50, null=True, unique=True)),
                ('status', models.BooleanField(blank=True, default=True, null=True)),
                ('state', models.CharField(max_length=50)),
                ('city', models.CharField(max_length=50)),
                ('addres', models.TextField(blank=True, null=True, verbose_name='Address')),
                ('pincode', models.PositiveIntegerField()),
                ('license_purchased', models.PositiveIntegerField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='company_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-id',),
            },
        ),
    ]
