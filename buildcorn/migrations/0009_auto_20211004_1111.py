# Generated by Django 3.2.5 on 2021-10-04 11:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('buildcorn', '0008_report'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='pic',
        ),
        migrations.RemoveField(
            model_name='question',
            name='reason',
        ),
        migrations.RemoveField(
            model_name='question',
            name='status',
        ),
        migrations.CreateModel(
            name='AnswerChecklist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(blank=True, choices=[('Compiled', 'Compiled'), ('Not Compiled', 'Not Compiled')], max_length=20, null=True)),
                ('reason', models.TextField(blank=True, null=True)),
                ('pic', models.ImageField(blank=True, null=True, upload_to='images/answer/%Y/%m/%d', verbose_name='Inspection pic')),
                ('quality_checklist', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='buildcorn.qualitychecklist')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='buildcorn.question')),
                ('safety_checklist', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='buildcorn.safetychecklist')),
            ],
            options={
                'ordering': ('-id',),
            },
        ),
    ]
