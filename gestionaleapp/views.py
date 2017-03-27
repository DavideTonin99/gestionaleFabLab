from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Person


# Create your views here.


@login_required
def customers(request):
	context = {
		'clients': Person.objects.all()
	}
	return render(request, 'gestionaleapp/anagrafica.html', context)


@login_required
def events(request):
	context = {
		'clients': Person.objects.all()
	}
	return render(request, 'gestionaleapp/eventi.html', context)


@login_required
def processings(request):
	context = {
		'clients': Person.objects.all()
	}
	return render(request, 'gestionaleapp/lavorazioni.html', context)


def get_client_data(request):
	if request.method == 'GET':
		id_ = request.GET.get('id', False)
		if not id_:
			return HttpResponseBadRequest(request)

		client = get_object_or_404(Person.objects.filter(id=id_))
		data = {
			'card': client.card,
			'surname': client.surname,
			'name': client.name,
			'born': client.born,
			'cap': client.cap,
			'telephone': client.telephone,
			'email': client.email
		}
		return JsonResponse(data)
