# Generated by Django 5.1.5 on 2025-02-22 01:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('epr', '0003_jobvacancy_published'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobApplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('confirm_email', models.EmailField(max_length=254)),
                ('phone_number', models.CharField(max_length=15)),
                ('place_of_residence', models.CharField(max_length=100)),
                ('message', models.TextField()),
                ('cv', models.FileField(upload_to='cvs/')),
                ('submitted_at', models.DateTimeField(auto_now_add=True)),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applications', to='epr.jobvacancy')),
            ],
        ),
    ]
