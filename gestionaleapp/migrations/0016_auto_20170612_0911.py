# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-12 07:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestionaleapp', '0015_auto_20170426_1553'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='cap',
            field=models.IntegerField(verbose_name='CAP'),
        ),
        migrations.AlterField(
            model_name='person',
            name='card',
            field=models.IntegerField(unique=True, verbose_name='Tessera'),
        ),
        migrations.AlterField(
            model_name='person',
            name='telephone',
            field=models.BigIntegerField(verbose_name='Cellulare'),
        ),
    ]