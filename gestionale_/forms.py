from django.forms import ModelForm

from .models import Customer, Subscription


class CustomerForm(ModelForm):
	class Meta:
		model = Customer
		fields = '__all__'

	def __init__(self, *args, **kwargs):
		super(CustomerForm, self).__init__(*args, **kwargs)

		for field in self.fields.values():
			field.widget.attrs['class'] = "form-control"


class SubscriptionForm(ModelForm):
	class Meta:
		model = Subscription
		exclude = ['year', 'customer']

	def __init__(self, *args, **kwargs):
		super(SubscriptionForm, self).__init__(*args, **kwargs)

		for field in self.fields.values():
			field.widget.attrs['class'] = "form-control"
