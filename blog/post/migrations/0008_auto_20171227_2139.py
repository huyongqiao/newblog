# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-27 13:39
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0007_remove_article_collector_id'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Collection',
            new_name='Collect',
        ),
    ]
