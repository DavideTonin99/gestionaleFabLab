# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-20 17:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestionaleapp', '0005_auto_20170320_1843'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='participants',
            field=models.ManyToManyField(blank=True, to='gestionaleapp.Person'),
        ),
    ]
