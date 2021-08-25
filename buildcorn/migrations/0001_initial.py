# Generated by Django 3.2.5 on 2021-08-25 07:25

import buildcorn.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CheckList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('checklist_id', models.CharField(default=buildcorn.models.licenseid, max_length=30)),
                ('text', models.TextField(default='its a verified list')),
                ('name', models.CharField(max_length=120)),
            ],
        ),
        migrations.CreateModel(
            name='SafetyLibrary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, null=True)),
                ('status', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=120)),
                ('quality_type', models.CharField(choices=[('quality', 'Quality'), ('safety', 'Safety')], max_length=10)),
                ('check_list', models.ManyToManyField(to='buildcorn.CheckList')),
            ],
        ),
        migrations.CreateModel(
            name='QualityLibrary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, null=True)),
                ('status', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=120)),
                ('quality_type', models.CharField(choices=[('quality', 'Quality'), ('safety', 'Safety')], max_length=10)),
                ('check_list', models.ManyToManyField(to='buildcorn.CheckList')),
            ],
        ),
        migrations.CreateModel(
            name='License',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('designation', models.CharField(blank=True, max_length=50, null=True)),
                ('license_id', models.CharField(default=buildcorn.models.licenseid, max_length=20)),
                ('created_at', models.DateField(auto_now_add=True, null=True, verbose_name='Start Date')),
                ('end_at', models.DateField(blank=True, null=True, verbose_name='End Date')),
                ('tenure', models.FloatField(blank=True, default=0, null=True)),
                ('status', models.BooleanField(default=False)),
                ('user_info', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]