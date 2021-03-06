# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-11-06 01:15
from __future__ import unicode_literals

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
            name='Class',
            fields=[
                ('class_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
                ('time', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('course_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('plan', models.TextField(blank=True)),
                ('book', models.TextField(blank=True)),
                ('background', models.TextField(blank=True)),
                ('exam', models.TextField(blank=True)),
                ('knowledge', models.TextField(blank=True)),
                ('project', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Finish',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('upload_time', models.DateTimeField()),
                ('files', models.FileField(upload_to='homework/')),
                ('score', models.IntegerField()),
                ('evaluation', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Homework',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20)),
                ('content', models.TextField()),
                ('files', models.FileField(upload_to='resource/homework/')),
                ('ddl', models.DateTimeField()),
                ('classes', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='display.Class')),
            ],
        ),
        migrations.CreateModel(
            name='Information',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('content', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Join',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('classes', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='display.Class')),
            ],
        ),
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('address', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('content', models.TextField()),
                ('classes', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='display.Class')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('school_id', models.CharField(max_length=20)),
                ('question', models.CharField(max_length=50)),
                ('answer', models.CharField(max_length=50)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('files', models.FileField(upload_to='resource/')),
                ('simple_file', models.FileField(upload_to='resource/')),
                ('classes', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='display.Class')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('experience', models.TextField(blank=True)),
                ('research', models.TextField(blank=True)),
                ('style', models.TextField(blank=True)),
                ('publication', models.TextField(blank=True)),
                ('honor', models.TextField(blank=True)),
                ('contact', models.TextField(blank=True)),
                ('other', models.TextField(blank=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Teaches',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('classes', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='display.Class')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='display.Teacher')),
            ],
        ),
        migrations.AddField(
            model_name='join',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='display.Student'),
        ),
        migrations.AddField(
            model_name='information',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='display.Teacher'),
        ),
        migrations.AddField(
            model_name='finish',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='display.Student'),
        ),
        migrations.AddField(
            model_name='class',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='display.Course'),
        ),
    ]
