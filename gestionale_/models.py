from datetime import date

from django.core.validators import RegexValidator, MinValueValidator
from django.db import models

CARD_PREFIX = 'VRFL'

SUBSCRIPTION_TYPE_CHOICES = ((0, 'Base'), (1, 'Maker'))
SUBSCRIPTION_PAYMENT_CHOICES = ((0, 'Paypal'), (1, 'Bonifico'), (2, 'Contanti'))
PROCESSING_TYPE_CHOICES = ((0, 'Laser'), (1, 'Stampa 3D'), (2, 'Fresa'))

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
	telephone = models.CharField(verbose_name='Cellulare', default='+39', validators=[phone_regex], max_length=16)
	email = models.EmailField(null=True, blank=True)
	card = models.CharField(verbose_name='Tessera', default=CARD_PREFIX, validators=[card_regex], max_length=9,
	                        unique=True)
	first_association = models.DateField(verbose_name='Data associazione', default=date.today)

	def __str__(self):
		return ' '.join((self.card, self.name.capitalize(), self.surname.capitalize()))


class Event(models.Model):
	class Meta:
		verbose_name = 'Evento'
		verbose_name_plural = 'Eventi'

	participants = models.ManyToManyField(Customer, verbose_name='Partecipanti', blank=True)
	name = models.CharField(verbose_name='Nome', max_length=200)
	date = models.DateField(verbose_name='Data', default=date.today)
	duration = models.PositiveSmallIntegerField(verbose_name='Durata (ore)')
	price = models.DecimalField(verbose_name='Prezzo', max_digits=6, decimal_places=2,
	                            validators=[MinValueValidator(0)], null=True, blank=True)
	description = models.CharField(verbose_name='Descrizione', max_length=1000, null=True, blank=True)

	def __str__(self):
		return self.name[:32] + '...'


class Subscription(models.Model):
	class Meta:
		verbose_name = 'Iscrizione'
		verbose_name_plural = 'Iscrizioni'

	customer = models.ForeignKey(Customer, verbose_name='Cliente', unique_for_year='year', on_delete=models.CASCADE)
	date = models.DateField(verbose_name='Data', default=date.today, validators=[])
	type = models.PositiveSmallIntegerField(verbose_name='Tipo', choices=SUBSCRIPTION_TYPE_CHOICES)
	payment = models.PositiveSmallIntegerField(verbose_name='Pagamento', choices=SUBSCRIPTION_PAYMENT_CHOICES)
	occasion = models.ForeignKey(Event, verbose_name='Occasione', null=True, blank=True, on_delete=models.SET_NULL)

	def __str__(self):
		return ', '.join(('Iscrizione', self.customer.name, str(self.date.year)))


class Processing(models.Model):
	class Meta:
		verbose_name = 'Lavorazione'
		verbose_name_plural = 'Lavorazioni'

	date = models.DateField(verbose_name='Data', default=date.today)
	customer = models.ForeignKey(Customer, verbose_name='Cliente', on_delete=models.CASCADE)
	type = models.PositiveSmallIntegerField(verbose_name='Tipo', choices=PROCESSING_TYPE_CHOICES)
	price = models.DecimalField(verbose_name='Prezzo', max_digits=6, decimal_places=2,
	                            validators=[MinValueValidator(0)], null=True, blank=True)
	description = models.CharField(verbose_name='Descrizione', max_length=1000, null=True, blank=True)

	def __str__(self):
		return ' '.join((str(self.type), str(self.customer), str(self.date)))
