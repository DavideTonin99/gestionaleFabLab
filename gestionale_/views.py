import csv
from datetime import date
from io import StringIO

from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms.forms import NON_FIELD_ERRORS
from django.forms.utils import ErrorList
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.shortcuts import reverse, get_object_or_404
from django.views.generic import CreateView, UpdateView

from .forms import CustomerForm, SubscriptionForm, EventForm, ProcessingForm
from .models import Customer, Subscription, Event, Processing


class CreateCustomerView(LoginRequiredMixin, CreateView):
	model = Customer
	form_class = CustomerForm

	def get_success_url(self):
		return reverse('gestionale_:update_customer', args=(self.object.id,))

	def get_context_data(self, **kwargs):
		context = super(CreateCustomerView, self).get_context_data(**kwargs)

		customers = self.model.objects.all()
		context['customers'] = [(customer, get(customer.subscription_set.filter(year__year=date.today().year), 0))
		                        for customer in customers]

		context['op'] = 'Crea'
		context['search_homonyms'] = True

		return context


class UpdateCustomerView(LoginRequiredMixin, UpdateView):
	model = Customer
	form_class = CustomerForm

	def get_success_url(self):
		return reverse('gestionale_:update_customer', args=(self.kwargs.get('customer_id'),))

	def get_object(self, queryset=None):
		return get_object_or_404(self.model.objects.filter(id=self.kwargs.get('customer_id')))

	def get_context_data(self, **kwargs):
		context = super(UpdateCustomerView, self).get_context_data(**kwargs)
		context['customers'] = [(customer, get(customer.subscription_set.filter(year__year=date.today().year), 0))
		                        for customer in self.model.objects.all()]
		context['op'] = 'Modifica'
		context['id'] = self.object.id

		all_subs = self.object.subscription_set.all()

		context['show_tables'] = True
		context['subscriptions'] = filter_queryset_in_years(all_subs, 2014, 2028)
		context['processings'] = self.object.processing_set.all()
		context['events'] = self.object.event_set.all()

		return context


class CreateSubscriptionView(LoginRequiredMixin, CreateView):
	model = Subscription
	form_class = SubscriptionForm

	def get_success_url(self):
		return reverse('gestionale_:update_subscription', args=(self.object.customer.id, self.object.id))

	def get_context_data(self, **kwargs):
		context = super(CreateSubscriptionView, self).get_context_data(**kwargs)
		context['op'] = 'Crea'

		customer = get_customer(self.kwargs.get('customer_id'))
		context['id'] = customer.id
		context['customer_name'] = str(customer)
		context['year'] = self.kwargs.get('year')

		all_subs = customer.subscription_set.all()
		context['subscriptions'] = filter_queryset_in_years(all_subs, 2014, 2028)

		return context

	def form_valid(self, form):
		form.instance.customer = get_customer(self.kwargs.get('customer_id'))

		year = self.kwargs.get('year')
		valid = False
		if year:
			try:
				year = date(day=1, month=1, year=int(year))
				form.instance.year = year
				valid = True
			except ValueError:
				pass

		valid = valid and not bool(len(self.model.objects.filter(customer=form.instance.customer,
		                                                         year__year=year.year)))

		if not valid:
			errors = form.errors.setdefault(NON_FIELD_ERRORS, ErrorList())
			errors.append("Anno non valido")
			return super(CreateSubscriptionView, self).form_invalid(form)

		return super(CreateSubscriptionView, self).form_valid(form)


class UpdateSubscriptionView(LoginRequiredMixin, UpdateView):
	model = Subscription
	form_class = SubscriptionForm

	def get_success_url(self):
		return reverse('gestionale_:update_subscription', args=(self.object.customer.id, self.object.id))

	def get_object(self, queryset=None):
		return get_object_or_404(get_customer(self.kwargs.get('customer_id')).
		                         subscription_set.filter(id=self.kwargs.get('subscription_id')))

	def get_context_data(self, **kwargs):
		context = super(UpdateSubscriptionView, self).get_context_data(**kwargs)
		context['op'] = 'Modifica'
		context['id'] = self.object.customer.id
		context['customer_name'] = str(self.object.customer)
		context['year'] = self.object.year.year

		all_subs = self.object.customer.subscription_set.all()
		context['subscriptions'] = filter_queryset_in_years(all_subs, 2014, 2028)

		return context


class CreateEventView(LoginRequiredMixin, CreateView):
	model = Event
	form_class = EventForm

	def get_success_url(self):
		return reverse('gestionale_:update_event', args=(self.object.id,))

	def get_context_data(self, **kwargs):
		context = super(CreateEventView, self).get_context_data(**kwargs)

		context['events'] = self.model.objects.all()
		context['op'] = 'Crea'

		return context


class UpdateEventView(LoginRequiredMixin, UpdateView):
	model = Event
	form_class = EventForm

	def get_success_url(self):
		return reverse('gestionale_:update_event', args=(self.object.id,))

	def get_object(self, queryset=None):
		return get_object_or_404(self.model.objects.filter(id=self.kwargs.get('event_id')))

	def get_context_data(self, **kwargs):
		context = super(UpdateEventView, self).get_context_data(**kwargs)

		context['events'] = self.model.objects.all()
		context['op'] = 'Modifica'

		return context


class CreateProcessingView(LoginRequiredMixin, CreateView):
	model = Processing
	form_class = ProcessingForm

	def get_success_url(self):
		return reverse('gestionale_:update_processing', args=(self.object.id,))

	def get_context_data(self, **kwargs):
		context = super(CreateProcessingView, self).get_context_data(**kwargs)

		context['processings'] = self.model.objects.all()
		context['op'] = 'Crea'

		return context


class UpdateProcessingView(LoginRequiredMixin, UpdateView):
	model = Processing
	form_class = ProcessingForm

	def get_success_url(self):
		return reverse('gestionale_:update_processing', args=(self.object.id,))

	def get_object(self, queryset=None):
		return get_object_or_404(self.model.objects.filter(id=self.kwargs.get('processing_id')))

	def get_context_data(self, **kwargs):
		context = super(UpdateProcessingView, self).get_context_data(**kwargs)

		context['processings'] = self.model.objects.all()
		context['op'] = 'Modifica'

		return context


def get_participants_emails_csv(request, event_id):
	event = get_object_or_404(Event.objects.filter(id=event_id))

	output = StringIO()
	csv.writer(output).writerows([participant.email] for participant in event.participants.all())
	content = output.getvalue()

	response = HttpResponse(content, content_type='text/csv')
	response['Content-Disposition'] = 'inline; filename="{}.csv"'.format(event.name or event.id)
	response['Content-Length'] = len(content)

	return response


def get_homonyms(request):
	try:
		assert request.method == 'POST'

		name, surname = request.POST.get('name'), request.POST.get('surname')
		assert bool(name) and bool(surname)

		return JsonResponse({
			'results': [[str(customer), reverse('gestionale_:update_customer', args=(customer.id,))]
			            for customer in Customer.objects.filter(name__istartswith=name, surname__istartswith=surname)]
		})
	except AssertionError:
		return HttpResponseBadRequest()


def filter_queryset_in_years(queryset, from_, to):
	return {year: get(queryset.filter(year__year=year), 0) for year in range(from_, to + 1)}


def get_customer(id_):
	return get_object_or_404(Customer.objects.filter(id=id_))


def get(k, i, default=None):
	try:
		return k[i]
	except IndexError:
		return default
