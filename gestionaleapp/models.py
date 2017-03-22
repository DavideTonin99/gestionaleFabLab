from django.db import models

# Create your models here.


class Person(models.Model):
	name = models.CharField(max_length=50)
	surname = models.CharField(max_length=50)
	born = models.DateTimeField("born date")
	cap = models.CharField(max_length=5)
	telephone = models.CharField(max_length=15)
	email = models.CharField(max_length=254)
	card = models.CharField(max_length=128)

	def __str__(self):
		return self.name.capitalize() + ' ' + self.surname.capitalize()


class Event(models.Model):
	participants = models.ManyToManyField(Person, blank=True)
	name = models.CharField(max_length=200)
	date = models.DateTimeField("event date")
	cost = models.PositiveIntegerField(null=True, blank=True)
	description = models.CharField(max_length=1000, null=True, blank=True)


class Subscription(models.Model):
	person = models.ForeignKey(Person, on_delete=models.CASCADE)
	year = models.PositiveSmallIntegerField()
	type = models.CharField(max_length=11)
	occasion = models.ForeignKey(Event, null=True, blank=True, on_delete=models.SET_NULL)


class Processing(models.Model):
	type = models.CharField(max_length=100)
	data = models.DateTimeField("processing date")
	cost = models.PositiveSmallIntegerField()
	description = models.CharField(max_length=1000, null=True, blank=True)
	person = models.ForeignKey(Person, on_delete=models.CASCADE, null=True)
