# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-29 04:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0010_user_icon'),
    ]

    operations = [
        migrations.CreateModel(
            name='Friend',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('user_id', models.IntegerField()),
                ('friend_id', models.IntegerField()),
            ],
        ),
    ]
