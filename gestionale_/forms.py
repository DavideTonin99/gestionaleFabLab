from django.core.exceptions import ValidationError
from django.forms import ModelForm

from .models import Customer, Subscription, Event, Processing


class CustomerForm(ModelForm):
	class Meta:
		model = Customer
		fields = '__all__'

	def __init__(self, *args, **kwargs):
		super(CustomerForm, self).__init__(*args, **kwargs)

		for field in self.fields.values():
			field.widget.attrs['class'] = 'form-control'


class SubscriptionForm(ModelForm):
	class Meta:
		model = Subscription
		exclude = ['customer']

	def __init__(self, *args, **kwargs):
		extras = kwargs.get('extras')

		if extras:
			del kwargs['extras']

		super(SubscriptionForm, self).__init__(*args, **kwargs)

		if extras:
			self.instance.customer = extras['customer']
			self.instance.start_date = extras['start_date']
			self.instance.end_date = extras['end_date']

		for field in self.fields.values():
			field.widget.attrs['class'] = 'form-control'

	def clean(self):
		if self.instance.start_date.year == self.instance.end_date.year:
			if self.instance.start_date.year > Subscription.SYS_CHANGE_YEAR:
				raise ValidationError('Periodo invalido')


class EventForm(ModelForm):
	class Meta:
		model = Event
		fields = '__all__'

	def __init__(self, *args, **kwargs):
		super(EventForm, self).__init__(*args, **kwargs)

		for field in self.fields.values():
			field.widget.attrs['class'] = 'form-control'


class ProcessingForm(ModelForm):
	class Meta:
		model = Processing
		fields = '__all__'

	def __init__(self, *args, **kwargs):
		super(ProcessingForm, self).__init__(*args, **kwargs)

		for field in self.fields.values():
			field.widget.attrs['class'] = 'form-control'
