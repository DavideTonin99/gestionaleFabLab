# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-20 17:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestionaleapp', '0008_auto_20170320_1849'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='cost',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='description',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='processing',
            name='description',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='occasion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='gestionaleapp.Event'),
        ),
    ]