from django.db import models

# Create your models here.


class Person(models.Model):
	name = models.CharField(max_length=50)
	surname = models.CharField(max_length=50)
	born = models.DateTimeField("born date")
	cap = models.DecimalField(max_digits=5, decimal_places=5)
	telephone = models.DecimalField(max_digits=15)
	email = models.CharField(max_length=254)
	card = models.CharField(max_length=128)

	def __str__(self):
		return self.name.capitalize() + ' ' + self.surname.capitalize()


class Event(models.Model):
	participant = models.ManyToManyField(Person, null=True)
	name = models.CharField(max_length=200)
	date = models.DateTimeField("event date")
	cost = models.IntegerField()
	description = models.CharField(max_length=1000)


class Subscription(models.Model):
	person = models.ForeignKey(Person)
	year = models.PositiveSmallIntegerField()
	type = models.CharField(max_length=10)
	occasion = models.ForeignKey(Event, null=True)


class Processing(models.Model):
	type = models.CharField(max_length=100)
	data = models.DateTimeField("processing date")
	cost = models.PositiveSmallIntegerField()
	description = models.CharField(max_length=1000)
	person = models.ManyToManyField(Person, null=True)
