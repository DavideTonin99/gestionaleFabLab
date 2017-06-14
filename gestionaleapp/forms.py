from django import forms

from .models import Person, Event, Processing


class CustomersForm(forms.ModelForm):  # todo born date format error; fix widgets not displaying correctly
    modify_id = forms.Field(widget=forms.HiddenInput(), initial='no')

    class Meta:
        model = Person
        fields = '__all__'
        labels = {
            'name': 'Nome',
            'surname': 'Cognome',
            'born': 'Nato',
            'cap': 'C.A.P',
            'telephone': 'Cellulare',
            'email': 'Mail',
            'card': 'Tessera',
        }

    def __init__(self, *args, **kwargs):
        super(CustomersForm, self).__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs['placeholder'] = field.label
            field.widget.attrs['class'] = "form-control"


class ProcessingsForm(forms.ModelForm):
    class Meta:
        model = Processing
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ProcessingsForm, self).__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs['placeholder'] = field.label
            field.widget.attrs['class'] = "form-control"


class EventsForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(EventsForm, self).__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs['class'] = "form-control"
