# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-20 17:42
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gestionaleapp', '0003_auto_20170320_1826'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='participant',
            new_name='participants',
        ),
    ]