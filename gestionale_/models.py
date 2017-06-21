from django.db import models
from django.core.validators import RegexValidator
from datetime import date

cap_regex = RegexValidator(regex=r'^\d{5}$', message='CAP non valido')
card_regex = RegexValidator(regex=r'^VRFL\d{5}$', message='Tessera non valida')
phone_regex = RegexValidator(regex=r'^\+?\d{8,15}$', message='Numero di telefono non valido')


class Customer(models.Model):
	class Meta:
		verbose_name = 'Cliente'
		verbose_name_plural = 'Clienti'

	name = models.CharField(verbose_name='Nome', max_length=50)
	surname = models.CharField(verbose_name='Cognome', max_length=50)
	born = models.DateField(verbose_name='Data di nascita')
	cap = models.CharField(verbose_name='CAP', validators=[cap_regex], max_length=5)
	telephone = models.CharField(verbose_name='Cellulare', default='+39', validators=[phone_regex], max_length=17)
	email = models.EmailField(null=True, blank=True)
	card = models.CharField(verbose_name='Tessera', default='VRFL', validators=[card_regex], max_length=9, unique=True)
	first_association = models.DateField(verbose_name='Data associazione', default=date.today)

	def __str__(self):
		return ' '.join((self.name.capitalize(), self.surname.capitalize()))


class Event(models.Model):
	class Meta:
		verbose_name = 'Evento'
		verbose_name_plural = 'Eventi'

	participants = models.ManyToManyField(Customer, verbose_name='Partecipanti', blank=True)
	name = models.CharField(verbose_name='Nome', max_length=200)
	date = models.DateTimeField(verbose_name='Data')
	cost = models.DecimalField(verbose_name='Costo', max_digits=6, decimal_places=2, null=True, blank=True)
	description = models.CharField(verbose_name='Descrizione', max_length=1000, null=True, blank=True)

	def __str__(self):
		return self.name[:12] + '...'


class Subscription(models.Model):
	class Meta:
		verbose_name = 'Iscrizione'
		verbose_name_plural = 'Iscrizioni'

	customer = models.ForeignKey(Customer, verbose_name='Cliente', unique_for_year='year', on_delete=models.CASCADE)
	year = models.DateField(verbose_name='Anno', default=date.today)
	type = models.PositiveSmallIntegerField(verbose_name='Tipo', choices=((0, 'BASE'), (1, 'MAKER')))
	occasion = models.ForeignKey(Event, verbose_name='Occasione', null=True, blank=True, on_delete=models.SET_NULL)

	def __str__(self):
		return ', '.join(('Iscrizione', self.customer.name, str(self.year.year)))


class Processing(models.Model):
	class Meta:
		verbose_name = 'Lavorazione'
		verbose_name_plural = 'Lavorazioni'

	data = models.DateField(verbose_name='Data', default=date.today)
	customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
	type = models.CharField(verbose_name='Tipo', max_length=100)
	cost = models.DecimalField(verbose_name='Costo', max_digits=6, decimal_places=2, null=True, blank=True)
	description = models.CharField(verbose_name='Descrizione', max_length=1000, null=True, blank=True)

	def __str__(self):
		return self.type
