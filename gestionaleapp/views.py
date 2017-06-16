from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView

from .models import Person, Event, Processing
from .forms import CustomersForm, ProcessingsForm, EventsForm


class CustomersView(LoginRequiredMixin, FormView):
    template_name = 'gestionaleapp/anagrafica.html'
    form_class = CustomersForm

    def get_success_url(self):
        return reverse('gestionale:anagrafica')

    def get_context_data(self, **kwargs):
        context = super(CustomersView, self).get_context_data(**kwargs)
        context['clients'] = Person.objects.all()
        return context

    def form_valid(self, form):
        modify_id = form.data.get('modify-id')
        if modify_id and modify_id.isnumeric():
            form = CustomersForm(form.cleaned_data, instance=get_object_or_404(Person.objects.filter(id=modify_id)))
        form.save()
        return super(CustomersView, self).form_valid(form)



class ProcessingsView(LoginRequiredMixin, FormView):
    template_name = 'gestionaleapp/lavorazioni.html'
    form_class = ProcessingsForm

    def get_success_url(self):
        return reverse('gestionale:lavorazioni')

    def get_context_data(self, **kwargs):
        context = super(ProcessingsView, self).get_context_data(**kwargs)
        context['processings'] = Processing.objects.all()
        return context

    def form_valid(self, form):
        form = ProcessingsForm()
        form.save()
        return super(ProcessingsView, self).form_valid(form)


class EventsView(LoginRequiredMixin, FormView):
    template_name = 'gestionaleapp/eventi.html'
    form_class = EventsForm

    def get_success_url(self):
        return reverse('gestionale:eventi')

    def get_context_data(self, **kwargs):
        context = super(EventsView, self).get_context_data(**kwargs)
        context['events'] = Event.objects.all()
        return context

    def form_valid(self, form):
        form = EventsForm()
        form.save()
        return super(EventsView, self).form_valid(form)


def wip(request):
    return HttpResponse("Work in progress")


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