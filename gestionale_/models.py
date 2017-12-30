from datetime import date
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, MinValueValidator
from django.db import models


class Customer(models.Model):
	CARD_PREFIX = 'VRFL'

	cap_regex = RegexValidator(regex=r'^\d{5}$', message='CAP non valido')
	card_regex = RegexValidator(regex=r'^VRFL\d{5}$', message='Tessera non valida')
	phone_regex = RegexValidator(regex=r'^\+?\d{8,15}$', message='Numero di telefono non valido')

	class Meta:
		verbose_name = 'Cliente'
		verbose_name_plural = 'Clienti'

	name = models.CharField(verbose_name='Nome', max_length=50)
	surname = models.CharField(verbose_name='Cognome', max_length=50)
	born = models.DateField(verbose_name='Data di nascita', null=True)
	cap = models.CharField(verbose_name='CAP', validators=[cap_regex], max_length=5, null=True)
	telephone = models.CharField(verbose_name='Cellulare', default='+39', validators=[phone_regex], max_length=16,
	                             null=True)
	email = models.EmailField(null=True)
	card = models.CharField(verbose_name='Tessera', default=CARD_PREFIX, validators=[card_regex], max_length=9,
	                        unique=True)
	first_association = models.DateField(verbose_name='Data associazione', default=date.today)
	card_given = models.NullBooleanField(verbose_name='Consegnata tessera')

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
	price = models.DecimalField(verbose_name='Prezzo', default=Decimal(0), max_digits=6, decimal_places=2,
	                            validators=[MinValueValidator(0)])
	description = models.CharField(verbose_name='Descrizione', max_length=1000, null=True, blank=True)

	def __str__(self):
		return self.name[:32] + '...'


class Subscription(models.Model):
	TYPE_CHOICES = enumerate(('Base', 'Maker'))
	PAYMENT_CHOICES = enumerate(('Paypal', 'Bonifico', 'Contanti'))

	class Meta:
		verbose_name = 'Iscrizione'
		verbose_name_plural = 'Iscrizioni'

	customer = models.ForeignKey(Customer, verbose_name='Cliente', on_delete=models.CASCADE)
	start_date = models.DateField(verbose_name='Data Inizio', default=date.today, validators=[])
	end_date = models.DateField(verbose_name='Data Fine', default=date.today, validators=[])
	type = models.PositiveSmallIntegerField(verbose_name='Tipo', choices=TYPE_CHOICES)
	payment = models.PositiveSmallIntegerField(verbose_name='Pagamento', choices=PAYMENT_CHOICES)
	occasion = models.ForeignKey(Event, verbose_name='Occasione', null=True, blank=True, on_delete=models.SET_NULL)

	def clean(self):
		if Subscription.objects.filter(customer=self.customer,
		                               start_date__lte=self.end_date,
		                               end_date__gte=self.start_date).exists():
			raise ValidationError('Iscrizione per questo periodo già esistente')

		super(Subscription, self).clean()

	def __str__(self):
		return ', '.join(('Iscrizione', self.customer.name, str(self.start_date.year)))


class Processing(models.Model):
	TYPE_CHOICES = enumerate(('Laser', 'Stampa 3D', 'Fresa'))

	class Meta:
		verbose_name = 'Lavorazione'
		verbose_name_plural = 'Lavorazioni'

	date = models.DateField(verbose_name='Data', default=date.today)
	customer = models.ForeignKey(Customer, verbose_name='Cliente', on_delete=models.CASCADE)
	type = models.PositiveSmallIntegerField(verbose_name='Tipo', choices=TYPE_CHOICES)
	materials_price = models.DecimalField(verbose_name='Prezzo materiali', max_digits=6, decimal_places=2,
	                                      validators=[MinValueValidator(0)], null=True, blank=True)
	machinery_price = models.DecimalField(verbose_name='Prezzo macchinari', max_digits=6, decimal_places=2,
	                                      validators=[MinValueValidator(0)], null=True, blank=True)
	description = models.CharField(verbose_name='Descrizione', max_length=1000, null=True, blank=True)

	def __str__(self):
		return ' '.join((str(self.type), str(self.customer), str(self.date)))
