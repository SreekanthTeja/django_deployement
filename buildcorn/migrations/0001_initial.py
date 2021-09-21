# Generated by Django 3.2.5 on 2021-09-20 13:26

import buildcorn.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('image', models.ImageField(upload_to='images/%Y/%m/%d')),
            ],
            options={
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='CheckList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('checklist_id', models.CharField(default=buildcorn.models.licenseid, max_length=30)),
                ('created_at', models.DateField(auto_now_add=True, null=True)),
                ('name', models.CharField(max_length=120)),
                ('typee', models.CharField(choices=[('Quality', 'Quality'), ('Safety', 'Safety')], max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='FAQ',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('faq_id', models.CharField(default=buildcorn.models.licenseid, max_length=50)),
                ('question', models.CharField(max_length=300)),
                ('answer', models.TextField(blank=True, null=True)),
                ('status', models.BooleanField(blank=True, default=False, null=True)),
            ],
            options={
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('checklist_id', models.CharField(default=buildcorn.models.licenseid, max_length=30)),
                ('question', models.TextField()),
                ('status', models.CharField(blank=True, choices=[('Compiled', 'Compiled'), ('Not Compiled', 'Not Compiled')], max_length=20, null=True)),
                ('reason', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True, null=True)),
                ('location', models.TextField()),
                ('inspection', models.CharField(blank=True, choices=[('D', 'Done'), ('P', 'Pending')], default='P', max_length=1, null=True)),
                ('approver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_approver', to=settings.AUTH_USER_MODEL)),
                ('checklists', models.ManyToManyField(blank=True, related_name='project_checklists', to='buildcorn.CheckList')),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.company', verbose_name='Company')),
                ('employee', models.ManyToManyField(blank=True, related_name='project_employees', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='License',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('license_id', models.CharField(default=buildcorn.models.licenseid, max_length=20)),
                ('created_at', models.DateField(blank=True, null=True, verbose_name='Start Date')),
                ('end_at', models.DateField(blank=True, null=True, verbose_name='End Date')),
                ('status', models.BooleanField(default=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('eid', models.CharField(default=buildcorn.models.licenseid, max_length=20)),
                ('created_at', models.DateField(auto_now_add=True, null=True)),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.company', verbose_name='employee_company')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='employee_user')),
            ],
            options={
                'ordering': ('-id',),
            },
        ),
        migrations.AddField(
            model_name='checklist',
            name='question',
            field=models.ManyToManyField(blank=True, to='buildcorn.Question'),
        ),
    ]
