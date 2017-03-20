from django.shortcuts import render

# Create your views here.

def anagrafica(request):
	return render(request, 'gestionaleapp/anagrafica.html')
