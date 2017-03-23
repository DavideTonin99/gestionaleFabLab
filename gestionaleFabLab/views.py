from django.shortcuts import render, reverse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout

# Create your views here.


def login_view(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect(reverse('gestionale:anagrafica'))
	context = {
		'next': request.GET.get('next', reverse('gestionale:anagrafica')),
		'wrong_login': request.GET.get('wrong_login', False)
	}
	return render(request, 'login.html', context)


def login_handler(request):
	username = request.POST['username']
	password = request.POST['password']
	user = authenticate(username=username, password=password)
	if user is not None:
		login(request, user)
		return HttpResponseRedirect(request.GET.get('next'))
	else:
		return HttpResponseRedirect(reverse('login') + '?next=' + request.GET.get('next') + ';wrong_login=True;')


def logout_handler(request):
	logout(request)
	return HttpResponseRedirect(request.GET.get('next'))
