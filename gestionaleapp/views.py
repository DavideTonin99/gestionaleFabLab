from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import FormView

from .models import Person
from .forms import CustomersForm


# Create your views here.


class CustomersView(FormView):
	template_name = 'gestionaleapp/anagrafica.html'
	form_class = CustomersForm
	success_url = reverse_lazy('gestionale:anagrafica')

	def get_context_data(self, **kwargs):
		context = super(CustomersView, self).get_context_data(**kwargs)
		context['clients'] = Person.objects.all()
		return context

	def form_valid(self, form):
		# todo save
		return super(CustomersView, self).form_valid(form)


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
