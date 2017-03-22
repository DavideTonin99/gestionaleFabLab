from django.shortcuts import render

from .models import Person

# Create your views here.


def anagrafica(request):
	context = {
		'clients': Person.objects.all()
	}
	return render(request, 'gestionaleapp/anagrafica.html', context)
