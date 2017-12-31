# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-26 09:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=50)),
                ('author', models.CharField(max_length=20)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('content', models.TextField()),
                ('read_count', models.IntegerField(default=0)),
                ('tag', models.CharField(max_length=50)),
                ('collector_id', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('author', models.CharField(max_length=20)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('content', models.TextField()),
                ('article_id', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=20, unique=True)),
                ('password_hash', models.CharField(max_length=128)),
                ('email', models.CharField(max_length=32, unique=True)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('confirmed', models.BooleanField(default=False)),
                ('friend_id', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'user',
            },
        ),
    ]
