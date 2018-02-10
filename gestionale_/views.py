import csv
from datetime import date
from decimal import Decimal
from io import StringIO

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.shortcuts import reverse, get_object_or_404
from django.views.generic import CreateView, UpdateView, TemplateView

from .forms import CustomerForm, SubscriptionForm, EventForm, ProcessingForm
from .models import Customer, Subscription, Event, Processing

CREATE = 'Salva'
MODIFY = 'Salva modifiche'


class CreateCustomerView(LoginRequiredMixin, CreateView):
	model = Customer
	form_class = CustomerForm

	def get_success_url(self):
		return reverse('gestionale_:update_customer', args=(self.object.id,))

	def get_initial(self):
		initial = super(CreateCustomerView, self).get_initial()

		customers = CreateCustomerView.model.objects.all()
		initial['card'] = str(max(customer.card for customer in customers) + 1 if customers.exists() else 0).zfill(5)

		return initial

	def get_context_data(self, **kwargs):
		context = super(CreateCustomerView, self).get_context_data(**kwargs)

		customers = CreateCustomerView.model.objects.all()
		for customer in customers:
			customer.subscribed = customer.subscription_set.filter(
				start_date__lte=date.today(),
				end_date__gte=date.today()
			).exists()

		today = date.today()

		context['op'] = CREATE
		context['customers'] = customers
		context['CARD_PREFIX'] = Customer.CARD_PREFIX
		context['current_period'] = \
			'{}/{}'.format(today.year - 1, today.year) if today < date(today.year, *Subscription.NEW_END_DATE) \
			else '{}/{}'.format(today.year, today.year + 1)

		context['search_homonyms'] = True

		return context


class UpdateCustomerView(LoginRequiredMixin, UpdateView):
	model = Customer
	form_class = CustomerForm

	def get_success_url(self):
		return reverse('gestionale_:update_customer', args=(self.object.id,))

	def get_initial(self):
		initial = super(UpdateCustomerView, self).get_initial()

		initial['cap'] = str(self.object.cap).zfill(5)
		initial['card'] = str(self.object.card).zfill(5)

		return initial

	def get_context_data(self, **kwargs):
		context = super(UpdateCustomerView, self).get_context_data(**kwargs)

		customers = UpdateCustomerView.model.objects.all()
		for customer in customers:
			customer.subscribed = customer.subscription_set.filter(
				start_date__lte=date.today(),
				end_date__gte=date.today()
			).exists()

		today = date.today()

		context['op'] = MODIFY
		context['id'] = self.object.id
		context['customers'] = customers
		context['subscriptions'] = {
			year: self.object.subscription_set.filter(start_date__year=year).first()
			for year in Subscription.YEARS_RANGE
		}
		context['events'] = self.object.event_set.all()
		context['processings'] = self.object.processing_set.all()
		context['CARD_PREFIX'] = Customer.CARD_PREFIX
		context['current_period'] = \
			'{}/{}'.format(today.year - 1, today.year) if today < date(today.year, *Subscription.NEW_END_DATE) \
			else '{}/{}'.format(today.year, today.year + 1)

		context['show_tables'] = True

		return context


class CreateSubscriptionView(LoginRequiredMixin, CreateView):
	model = Subscription
	form_class = SubscriptionForm

	def get_success_url(self):
		return reverse('gestionale_:update_subscription', args=(self.object.id,))

	def get_form_kwargs(self):
		extras = {
			'customer': get_object_or_404(Customer.objects.filter(id=self.kwargs['customer_id']))
		}

		start, end = map(int, self.kwargs['period'].split('/'))

		if start == end:
			extras['start_date'] = date(start, *Subscription.OLD_START_DATE)
			extras['end_date'] = date(end, *Subscription.OLD_END_DATE)
		else:
			extras['start_date'] = date(start, *Subscription.NEW_START_DATE)
			extras['end_date'] = date(end, *Subscription.NEW_END_DATE)

		kwargs = super(CreateSubscriptionView, self).get_form_kwargs()
		kwargs['extras'] = extras
		return kwargs

	def get_context_data(self, **kwargs):
		context = super(CreateSubscriptionView, self).get_context_data(**kwargs)

		customer = get_object_or_404(Customer.objects.filter(id=self.kwargs['customer_id']))
		start, end = self.kwargs['period'].split('/')

		context['op'] = CREATE
		context['id'] = customer.id
		context['subscriptions'] = {
			year: customer.subscription_set.filter(start_date__year=year).first()
			for year in Subscription.YEARS_RANGE
		}
		context['customer_name'] = str(customer)
		context['period'] = start if start == end else self.kwargs['period']

		return context


class UpdateSubscriptionView(LoginRequiredMixin, UpdateView):
	model = Subscription
	form_class = SubscriptionForm

	def get_success_url(self):
		return reverse('gestionale_:update_subscription', args=(self.object.id,))

	def get_context_data(self, **kwargs):
		context = super(UpdateSubscriptionView, self).get_context_data(**kwargs)

		context['op'] = MODIFY
		context['id'] = self.object.customer.id
		context['subscriptions'] = {
			year: self.object.customer.subscription_set.filter(start_date__year=year).first()
			for year in Subscription.YEARS_RANGE
		}
		context['customer_name'] = str(self.object.customer)
		context['period'] = self.object.period

		return context


class CreateEventView(LoginRequiredMixin, CreateView):
	model = Event
	form_class = EventForm

	def get_success_url(self):
		return reverse('gestionale_:update_event', args=(self.object.id,))

	def get_context_data(self, **kwargs):
		context = super(CreateEventView, self).get_context_data(**kwargs)

		context['op'] = CREATE
		context['events'] = CreateEventView.model.objects.all()

		return context


class UpdateEventView(LoginRequiredMixin, UpdateView):
	model = Event
	form_class = EventForm

	def get_success_url(self):
		return reverse('gestionale_:update_event', args=(self.object.id,))

	def get_context_data(self, **kwargs):
		context = super(UpdateEventView, self).get_context_data(**kwargs)

		context['op'] = MODIFY
		context['events'] = UpdateEventView.model.objects.all()

		return context


class CreateProcessingView(LoginRequiredMixin, CreateView):
	model = Processing
	form_class = ProcessingForm

	def get_success_url(self):
		return reverse('gestionale_:update_processing', args=(self.object.id,))

	def get_context_data(self, **kwargs):
		context = super(CreateProcessingView, self).get_context_data(**kwargs)

		context['op'] = CREATE
		context['processings'] = CreateProcessingView.model.objects.all()

		return context


class UpdateProcessingView(LoginRequiredMixin, UpdateView):
	model = Processing
	form_class = ProcessingForm

	def get_success_url(self):
		return reverse('gestionale_:update_processing', args=(self.object.id,))

	def get_context_data(self, **kwargs):
		context = super(UpdateProcessingView, self).get_context_data(**kwargs)

		context['op'] = MODIFY
		context['processings'] = UpdateProcessingView.model.objects.all()

		return context


class StatsView(LoginRequiredMixin, TemplateView):
	template_name = "gestionale_/stats.html"


@login_required
def get_participants_emails_csv(request, event_id):
	event = get_object_or_404(Event.objects.filter(id=event_id))

	output = StringIO()
	csv.writer(output).writerows((participant.email,) for participant in event.participants.all())
	content = output.getvalue()

	response = HttpResponse(content, content_type='text/csv')
	response['Content-Disposition'] = 'inline; filename="{}.csv"'.format(event.name or event.id)
	response['Content-Length'] = len(content)

	return response


@login_required
def get_customers_table_csv(request):
	output = StringIO()
	csv.writer(output).writerows((
		                             customer.surname,
		                             customer.name,
		                             '{}{:05d}'.format(Customer.CARD_PREFIX, customer.card),
		                             customer.email,
		                             customer.phone,
		                             'Sì' if customer.card_given else 'No',
		                             'Sì' if customer.subscription_set.filter(
			                             start_date__lte=date.today(),
			                             end_date__gte=date.today()
		                             ).exists() else 'No'
	                             ) for customer in Customer.objects.all())
	content = output.getvalue()

	response = HttpResponse(content, content_type='text/csv')
	response['Content-Disposition'] = 'inline; filename="customers.csv"'
	response['Content-Length'] = len(content)

	return response


@login_required
def get_events_table_csv(request):
	output = StringIO()
	csv.writer(output).writerows((
		                             event.date,
		                             event.duration,
		                             event.name,
		                             event.price,
		                             event.description
	                             ) for event in Event.objects.all())
	content = output.getvalue()

	response = HttpResponse(content, content_type='text/csv')
	response['Content-Disposition'] = 'inline; filename="events.csv"'
	response['Content-Length'] = len(content)

	return response


@login_required
def get_processings_table_csv(request):
	output = StringIO()
	csv.writer(output).writerows((
		                             processing.date,
		                             processing.customer,
		                             Processing.TYPE_CHOICES[processing.type][1],
		                             processing.price,
		                             processing.description
	                             ) for processing in Processing.objects.all())
	content = output.getvalue()

	response = HttpResponse(content, content_type='text/csv')
	response['Content-Disposition'] = 'inline; filename="processings.csv"'
	response['Content-Length'] = len(content)

	return response


@login_required
def get_homonyms(request):
	try:
		assert request.method == 'POST'

		name, surname = request.POST.get('name'), request.POST.get('surname')
		assert name and surname

	except AssertionError:
		return HttpResponseBadRequest()

	else:
		return JsonResponse({
			'results': [(str(customer), reverse('gestionale_:update_customer', args=(customer.id,)))
			            for customer in Customer.objects.filter(name__istartswith=name, surname__istartswith=surname)]
		})


@login_required
def get_associations_per_year(request):
	return JsonResponse({
		'categories': tuple(Subscription.YEARS_RANGE),
		'series': [{
			'name': description,
			'data': [len(Subscription.objects.filter(created__year=year, type=choice))
			         for year in Subscription.YEARS_RANGE]
		} for choice, description in Subscription.TYPE_CHOICES]})


@login_required
def get_associations_per_month(request):
	try:
		assert request.method == 'GET'

		year = int(request.GET.get('year'))

	except (AssertionError, TypeError):
		return HttpResponseBadRequest()

	else:
		months = range(1, 12 + 1)

		return JsonResponse({
			'categories': tuple(months),
			'series': [{
				'name': description,
				'data': [len(Subscription.objects.filter(created__year=year, created__month=month, type=choice))
				         for month in months]
			} for choice, description in Subscription.TYPE_CHOICES]})


@login_required
def get_renewals_for_year(request):
	return JsonResponse({
		'categories': tuple(Subscription.YEARS_RANGE),
		'series': [{
			'name': Subscription.RENEWED,
			'data': [sum(map(lambda sub: sub and Subscription.objects.filter(customer=sub.customer,
			                                                                 created__year=year - 1).exists(),
			                 Subscription.objects.filter(created__year=year))) for year in Subscription.YEARS_RANGE]
		}, {
			'name': Subscription.NON_RENEWED,
			'data': [sum(map(lambda sub: sub and not Subscription.objects.filter(customer=sub.customer,
			                                                                     created__year=year - 1).exists(),
			                 Subscription.objects.filter(created__year=year))) for year in Subscription.YEARS_RANGE]
		}]})


@login_required
def get_earnings_per_year(request):
	if request.method == 'GET':
		year = None

		try:
			year = int(request.GET.get('year'))

		except TypeError:
			pass

		if year:
			return JsonResponse({
				'labels': [description for _, description in Processing.TYPE_CHOICES],

				'datasets': [{
					'data': [sum((p.price for p in Processing.objects.filter(date__year=year, type=choice)),
					             Decimal('0.00'))
					         for choice, _ in Processing.TYPE_CHOICES]
				}]
			})

		else:
			return JsonResponse({
				'categories': tuple(Subscription.YEARS_RANGE),
				'series': [{
					'name': description,
					'data': [sum((p.price for p in Processing.objects.filter(date__year=year, type=choice)),
					             Decimal('0.00'))
					         for year in Subscription.YEARS_RANGE]
				} for choice, description in Processing.TYPE_CHOICES]})

	else:
		return HttpResponseBadRequest()
