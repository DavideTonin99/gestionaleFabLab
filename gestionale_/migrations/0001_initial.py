# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-07-01 01:36
from __future__ import unicode_literals

import datetime
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Nome')),
                ('surname', models.CharField(max_length=50, verbose_name='Cognome')),
                ('born', models.DateField(null=True, verbose_name='Data di nascita')),
                ('cap', models.CharField(max_length=5, null=True, validators=[django.core.validators.RegexValidator(message='CAP non valido', regex='^\\d{5}$')], verbose_name='CAP')),
                ('telephone', models.CharField(default='+39', max_length=16, validators=[django.core.validators.RegexValidator(message='Numero di telefono non valido', regex='^\\+?\\d{8,15}$')], verbose_name='Cellulare')),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('card', models.CharField(default='VRFL', max_length=9, unique=True, validators=[django.core.validators.RegexValidator(message='Tessera non valida', regex='^VRFL\\d{5}$')], verbose_name='Tessera')),
                ('first_association', models.DateField(default=datetime.date.today, verbose_name='Data associazione')),
            ],
            options={
                'verbose_name': 'Cliente',
                'verbose_name_plural': 'Clienti',
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Nome')),
                ('date', models.DateField(default=datetime.date.today, verbose_name='Data')),
                ('duration', models.PositiveSmallIntegerField(verbose_name='Durata (ore)')),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Prezzo')),
                ('description', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Descrizione')),
                ('participants', models.ManyToManyField(blank=True, to='gestionale_.Customer', verbose_name='Partecipanti')),
            ],
            options={
                'verbose_name': 'Evento',
                'verbose_name_plural': 'Eventi',
            },
        ),
        migrations.CreateModel(
            name='Processing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=datetime.date.today, verbose_name='Data')),
                ('type', models.PositiveSmallIntegerField(choices=[(0, 'Laser'), (1, 'Stampa 3D'), (2, 'Fresa')], verbose_name='Tipo')),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Prezzo')),
                ('description', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Descrizione')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestionale_.Customer', verbose_name='Cliente')),
            ],
            options={
                'verbose_name': 'Lavorazione',
                'verbose_name_plural': 'Lavorazioni',
            },
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=datetime.date.today, verbose_name='Data')),
                ('type', models.PositiveSmallIntegerField(choices=[(0, 'Base'), (1, 'Maker')], verbose_name='Tipo')),
                ('payment', models.PositiveSmallIntegerField(choices=[(0, 'Paypal'), (1, 'Bonifico'), (2, 'Contanti')], verbose_name='Pagamento')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestionale_.Customer', unique_for_year='year', verbose_name='Cliente')),
                ('occasion', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='gestionale_.Event', verbose_name='Occasione')),
            ],
            options={
                'verbose_name': 'Iscrizione',
                'verbose_name_plural': 'Iscrizioni',
            },
        ),
    ]
