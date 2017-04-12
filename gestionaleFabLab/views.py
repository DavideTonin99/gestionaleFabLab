from django.http import HttpResponseRedirect
from django.shortcuts import reverse


def index(request):
	return HttpResponseRedirect(reverse('gestionale:anagrafica'), request)
