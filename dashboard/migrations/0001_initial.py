# Generated by Django 3.2.5 on 2021-10-20 17:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('buildcorn', '0001_initial'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChecklistsUsage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('typee', models.CharField(choices=[('Quality', 'Quality'), ('Safety', 'Safety')], max_length=10)),
                ('name', models.CharField(max_length=50)),
                ('count', models.IntegerField(default=0)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.company')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='buildcorn.project')),
            ],
            options={
                'ordering': ('-id',),
            },
        ),
    ]
