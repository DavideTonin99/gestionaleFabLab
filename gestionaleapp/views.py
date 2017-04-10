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


@login_required
def get_client_data(request):
	id_ = request.GET.get('id', False)
	if not id_:
		return HttpResponseBadRequest(request)

	client = get_object_or_404(Person.objects.filter(id=id_))
	data = {
		'card': client.card,
		'surname': client.surname,
		'name': client.name,
		'born': '{}-{}-{}'.format(client.born.year, str(client.born.month).zfill(2), str(client.born.day).zfill(2)),
		'cap': client.cap,
		'telephone': client.telephone,
		'email': client.email,
		'subscriptions': {sub.year: sub.type for sub in client.subscription_set.all()}
	}
	return JsonResponse(data)


@login_required
def handle_client_data(request):
	data = request.POST
	print(data)
	return render(request, 'login.html')
