from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Person


# Create your views here.


@login_required
def anagrafica(request):
    context = {
        'clients': Person.objects.all()
    }
    return render(request, 'gestionaleapp/anagrafica.html', context)


@login_required
def eventi(request):
    context = {
        'clients': Person.objects.all()
    }
    return render(request, 'gestionaleapp/eventi.html', context)


@login_required
def lavorazioni(request):
    context = {
        'clients': Person.objects.all()
    }
    return render(request, 'gestionaleapp/lavorazioni.html', context)
