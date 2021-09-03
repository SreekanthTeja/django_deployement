# Generated by Django 3.2.5 on 2021-09-03 06:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_auto_20210903_0630'),
        ('buildcorn', '0003_auto_20210901_1007'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('date', models.DateField(blank=True, null=True)),
                ('phone', models.CharField(max_length=15)),
            ],
            options={
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('location', models.TextField()),
                ('typee', models.CharField(choices=[('Onsite', 'Onsite'), ('Offsite', 'Offsite')], max_length=10)),
                ('approver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_approver', to='buildcorn.employee')),
                ('comapany', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.company')),
                ('employee', models.ManyToManyField(blank=True, related_name='project_employee', to='buildcorn.Employee')),
            ],
            options={
                'ordering': ('-id',),
            },
        ),
    ]
