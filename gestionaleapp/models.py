import datetime

from django.db import models
from django.utils import timezone

# Create your models here.


class Person(models.Model):
	name = models.CharField(max_length=32)
	surname = models.CharField(max_length=32)
	born = models.DateTimeField("born date")
	cap = models.IntegerField()
	telephone = models.IntegerField()
	email = models.CharField(max_length=254)
	tessera = models.CharField(max_length=128)

	def __str__(self):
		return self.name.capitalize() + ' ' + self.surname.capitalize()


class Event(models.Model):
	participant = models.ForeignKey(Person)
	date = models.DateTimeField("event date")
	cost = models.IntegerField()
	description = models.CharField(max_length=64)		
