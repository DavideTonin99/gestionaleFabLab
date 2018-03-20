from datetime import date
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.db.models import Model, CharField, DateField, PositiveIntegerField, EmailField, NullBooleanField, \
	ManyToManyField, PositiveSmallIntegerField, DecimalField, ForeignKey, CASCADE, SET_NULL


class Customer(Model):
	CARD_PREFIX = 'VRFL'

	class Meta:
		verbose_name = 'Cliente'
		verbose_name_plural = 'Clienti'

	name = CharField(verbose_name='Nome', max_length=50)
	surname = CharField(verbose_name='Cognome', max_length=50)
	born = DateField(verbose_name='Data di nascita')
	cap = PositiveIntegerField(verbose_name='CAP', validators=[MaxValueValidator(99999, 'CAP non valido')])
	phone = CharField(verbose_name='Cellulare', default='+39', max_length=16,
	                  validators=[RegexValidator(r'^\+?\d{8,15}$', 'Numero di telefono non valido')])
	email = EmailField()
	card = PositiveIntegerField(verbose_name='Tessera', unique=True,
	                            validators=[MaxValueValidator(99999, 'Tessera non valida')])
	first_association = DateField(verbose_name='Data associazione', default=date.today)
	card_given = NullBooleanField(verbose_name='Consegnata tessera')

	def __str__(self):
		return ' '.join((Customer.CARD_PREFIX + str(self.card).zfill(5), self.name, self.surname))


class Event(Model):
	class Meta:
		verbose_name = 'Evento'
		verbose_name_plural = 'Eventi'

	participants = ManyToManyField(Customer, verbose_name='Partecipanti', blank=True)
	name = CharField(verbose_name='Nome', max_length=200)
	date = DateField(verbose_name='Data', default=date.today)
	duration = PositiveSmallIntegerField(verbose_name='Durata (ore)')
	price = DecimalField(verbose_name='Prezzo', default=Decimal(0), max_digits=6, decimal_places=2,
	                     validators=[MinValueValidator(0)])
	description = CharField(verbose_name='Descrizione', max_length=1000, blank=True)

	def __str__(self):
		return self.name[:32] + '...'


class Subscription(Model):
	TYPE_CHOICES = tuple(enumerate(('Base', 'Maker')))
	PAYMENT_CHOICES = tuple(enumerate(('Paypal', 'Bonifico', 'Contanti')))

	SYS_CHANGE_YEAR = 2016
	OLD_START_DATE = 1, 1
	OLD_END_DATE = 12, 31
	NEW_START_DATE = NEW_START_MONTH, _ = 9, 1
	NEW_END_DATE = NEW_END_MONTH, _ = 8, 31

	YEARS_RANGE = range(2014, 2028 + 1)

	# The lambda is a workaround because the conditional expression in the generator expression uses a different scope
	# from the class, and SYS_CHANGE_YEAR was not accessible.
	#
	# Consider the following line to be:
	# NESTED_YEARS_RANGE = tuple((year,) if year <= SYS_CHANGE_YEAR else (year, year + 1) for year in YEARS_RANGE)
	NESTED_YEARS_RANGE = (lambda sys_change_year=SYS_CHANGE_YEAR, years_range=YEARS_RANGE:
	                      tuple((year,) if year <= sys_change_year else (year, year + 1) for year in years_range))()

	RENEWED = 'Iscritti l\'anno precedente'
	NON_RENEWED = 'Non iscritti l\'anno precedente'

	class Meta:
		verbose_name = 'Iscrizione'
		verbose_name_plural = 'Iscrizioni'

	customer = ForeignKey(Customer, verbose_name='Cliente', on_delete=CASCADE)
	start_date = DateField(editable=False)
	end_date = DateField(editable=False)
	type = PositiveSmallIntegerField(verbose_name='Tipo', choices=TYPE_CHOICES)
	payment = PositiveSmallIntegerField(verbose_name='Pagamento', choices=PAYMENT_CHOICES)
	occasion = ForeignKey(Event, verbose_name='Occasione', null=True, blank=True, on_delete=SET_NULL)
	created = DateField(auto_now_add=True, editable=False)

	def clean(self):
		if not (self.start_date and self.end_date):
			raise ValidationError('Periodo invalido')

		if self.end_date < self.start_date:
			raise ValidationError('La data di fine del periodo è prima della data di inizio')

		if Subscription.objects.filter(customer=self.customer).exclude(pk=self.pk).filter(
				start_date__lte=self.end_date,
				end_date__gte=self.start_date
		).exists():
			raise ValidationError('Iscrizione per questo periodo già esistente')

	@property
	def period(self):
		if self.start_date.year != self.end_date.year:
			return '{}/{}'.format(self.start_date.year, self.end_date.year)
		else:
			return str(self.start_date.year)

	def __str__(self):
		return 'Iscrizione {} - {}'.format(self.customer.name, self.period)


class Processing(Model):
	TYPE_CHOICES = tuple(enumerate(('Laser', 'Stampa 3D', 'Fresa')))

	class Meta:
		verbose_name = 'Lavorazione'
		verbose_name_plural = 'Lavorazioni'

	date = DateField(verbose_name='Data', default=date.today)
	customer = ForeignKey(Customer, verbose_name='Cliente', on_delete=CASCADE)
	type = PositiveSmallIntegerField(verbose_name='Tipo', choices=TYPE_CHOICES)
	materials_price = DecimalField(verbose_name='Prezzo materiali', default=Decimal(0), max_digits=6, decimal_places=2,
	                               validators=[MinValueValidator(0)])
	machinery_price = DecimalField(verbose_name='Prezzo macchinari', default=Decimal(0), max_digits=6, decimal_places=2,
	                               validators=[MinValueValidator(0)])
	description = CharField(verbose_name='Descrizione', max_length=1000, blank=True)

	@property
	def price(self):
		return self.materials_price + self.machinery_price

	def __str__(self):
		return ' '.join(map(str, (self.type, self.customer, self.date)))
