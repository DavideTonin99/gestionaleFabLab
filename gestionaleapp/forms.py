from django import forms

from .models import Person

labels = ['Nome', 'Cognome', 'Nato', 'C.A.P', 'Cellulare', 'Mail', 'Tessera']
widgets = [
	#  todo validations
]


class CustomersForm(forms.ModelForm):
	class Meta:
		model = Person
		fields = ['name', 'surname', 'born', 'cap', 'telephone', 'email', 'card']

	def __init__(self, *args, **kwargs):
		super(CustomersForm, self).__init__(*args, **kwargs)
		for field, label in zip(self.fields, labels):
			field_ = self.fields[field]
			field_.label = label
			field_.widget.attrs['placeholder'] = label
			field_.widget.attrs['class'] = "cl-info-input form-control"
