from django import forms

from .models import Person


class ClientDataForm(forms.ModelForm):
	class Meta:
		model = Person
		fields = ['name', 'surname', 'born', 'cap', 'telephone', 'email', 'card']
