# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-20 17:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestionaleapp', '0002_auto_20170320_1819'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='cap',
            field=models.CharField(max_length=5),
        ),
    ]