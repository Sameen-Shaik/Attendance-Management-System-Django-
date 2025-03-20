# Generated by Django 5.1.5 on 2025-02-16 17:30

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authenticate', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('code', models.CharField(max_length=10, unique=True)),
                ('department', models.CharField(max_length=3)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CourseBatch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('term', models.CharField(help_text='Eg: 22 - Term -1', max_length=10, verbose_name='Batch and Term')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='attendance.course')),
                ('faculty', models.ManyToManyField(blank=True, to='authenticate.faculty')),
                ('students', models.ManyToManyField(blank=True, to='authenticate.student')),
            ],
        ),
        migrations.CreateModel(
            name='MySession',
            fields=[
                ('mysession_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('date', models.DateField(auto_now_add=True)),
                ('topic', models.CharField(blank=True, max_length=200, null=True)),
                ('course_batch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='attendance.coursebatch')),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('present', 'Present'), ('absent', 'Absent')], default='present', max_length=10)),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authenticate.student')),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='attendance.mysession')),
            ],
            options={
                'verbose_name_plural': 'Attendance Records',
                'unique_together': {('session', 'student')},
            },
        ),
    ]
