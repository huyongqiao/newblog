# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-26 11:27
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='article',
            table='article',
        ),
        migrations.AlterModelTable(
            name='comment',
            table='comment',
        ),
    ]
