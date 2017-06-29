import csv
from datetime import date
from decimal import Decimal
from io import StringIO

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.shortcuts import reverse, get_object_or_404
from django.views.generic import CreateView, UpdateView, TemplateView

from .forms import CustomerForm, SubscriptionForm, EventForm, ProcessingForm
from .models import Customer, Subscription, Event, Processing, \
	CARD_PREFIX, SUBSCRIPTION_TYPE_CHOICES, PROCESSING_TYPE_CHOICES

YEAR_BOUNDARIES = (2014, 2028)
CREATE = 'Crea'
MODIFY = 'Modifica'
RENEWED = 'Iscritti l\'anno precedente'
NON_RENEWED = 'Non iscritti l\'anno precedente'


class CreateCustomerView(LoginRequiredMixin, CreateView):
	model = Customer
	form_class = CustomerForm

	def get_success_url(self):
		return reverse('gestionale_:update_customer', args=(self.object.id,))

	def get_initial(self):
		initial = super(CreateCustomerView, self).get_initial()
		customers = Customer.objects.all()
		initial['card'] = CARD_PREFIX + '{0:05d}'.format(max(map(lambda x: int(x.card[4:]), customers)) + 1
		                                                 if customers else 0)
		return initial

	def get_context_data(self, **kwargs):
		context = super(CreateCustomerView, self).get_context_data(**kwargs)

		customers = self.model.objects.all()
		context['customers'] = [(customer, get(customer.subscription_set.filter(date__year=date.today().year), 0))
		                        for customer in customers]

		context['op'] = CREATE
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
		context['customers'] = [(customer, get(customer.subscription_set.filter(date__year=date.today().year), 0))
		                        for customer in self.model.objects.all()]
		context['op'] = MODIFY
		context['id'] = self.object.id

		all_subs = self.object.subscription_set.all()

		context['show_tables'] = True
		context['subscriptions'] = filter_queryset_in_years(all_subs, YEAR_BOUNDARIES[0], YEAR_BOUNDARIES[1])
		context['processings'] = self.object.processing_set.all()
		context['events'] = self.object.event_set.all()

		return context


class CreateSubscriptionView(LoginRequiredMixin, CreateView):
	model = Subscription
	form_class = SubscriptionForm

	def get_success_url(self):
		return reverse('gestionale_:update_subscription', args=(self.object.customer.id, self.object.id))

	def get_initial(self):
		today = date.today()
		initial = super(CreateSubscriptionView, self).get_initial()

		try:
			year = int(self.kwargs.get('year'))
			assert YEAR_BOUNDARIES[0] <= year <= YEAR_BOUNDARIES[1]
			initial['date'] = date(year, today.month, today.day).strftime(settings.DATE_INPUT_FORMATS[0])
		except (ValueError, TypeError, AssertionError):
			initial['date'] = ''

		return initial

	def get_context_data(self, **kwargs):
		context = super(CreateSubscriptionView, self).get_context_data(**kwargs)
		context['op'] = CREATE

		customer = get_object_or_404(Customer.objects.filter(id=self.kwargs.get('customer_id')))
		context['id'] = customer.id
		context['customer_name'] = str(customer)

		all_subs = customer.subscription_set.all()
		context['subscriptions'] = filter_queryset_in_years(all_subs, YEAR_BOUNDARIES[0], YEAR_BOUNDARIES[1])

		return context


class UpdateSubscriptionView(LoginRequiredMixin, UpdateView):
	model = Subscription
	form_class = SubscriptionForm

	def get_success_url(self):
		return reverse('gestionale_:update_subscription', args=(self.object.customer.id, self.object.id))

	def get_object(self, queryset=None):
		return get_object_or_404(get_object_or_404(Customer.objects.filter(id=self.kwargs.get('customer_id'))).
		                         subscription_set.filter(id=self.kwargs.get('subscription_id')))

	def get_context_data(self, **kwargs):
		context = super(UpdateSubscriptionView, self).get_context_data(**kwargs)
		context['op'] = MODIFY
		context['id'] = self.object.customer.id
		context['customer_name'] = str(self.object.customer)

		all_subs = self.object.customer.subscription_set.all()
		context['subscriptions'] = filter_queryset_in_years(all_subs, YEAR_BOUNDARIES[0], YEAR_BOUNDARIES[1])

		return context


class CreateEventView(LoginRequiredMixin, CreateView):
	model = Event
	form_class = EventForm

	def get_success_url(self):
		return reverse('gestionale_:update_event', args=(self.object.id,))

	def get_context_data(self, **kwargs):
		context = super(CreateEventView, self).get_context_data(**kwargs)

		context['events'] = self.model.objects.all()
		context['op'] = CREATE

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
		context['op'] = MODIFY

		return context


class CreateProcessingView(LoginRequiredMixin, CreateView):
	model = Processing
	form_class = ProcessingForm

	def get_success_url(self):
		return reverse('gestionale_:update_processing', args=(self.object.id,))

	def get_context_data(self, **kwargs):
		context = super(CreateProcessingView, self).get_context_data(**kwargs)

		context['processings'] = self.model.objects.all()
		context['op'] = CREATE

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
		context['op'] = MODIFY

		return context


class StatsView(LoginRequiredMixin, TemplateView):
	template_name = "gestionale_/stats.html"


@login_required
def get_participants_emails_csv(request, event_id):
	event = get_object_or_404(Event.objects.filter(id=event_id))

	output = StringIO()
	csv.writer(output).writerows([participant.email] for participant in event.participants.all())
	content = output.getvalue()

	response = HttpResponse(content, content_type='text/csv')
	response['Content-Disposition'] = 'inline; filename="{}.csv"'.format(event.name or event.id)
	response['Content-Length'] = len(content)

	return response


@login_required
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


@login_required
def get_associations_per_year(request):
	years = range(YEAR_BOUNDARIES[0], YEAR_BOUNDARIES[1] + 1)
	return JsonResponse({
		'categories': list(years),
		'series': [{
			'name': choice[1],
			'data': [len(Subscription.objects.filter(date__year=year, type=choice[0]))
			         for year in years]
		} for choice in SUBSCRIPTION_TYPE_CHOICES]})


@login_required
def get_associations_per_month(request):
	try:
		assert request.method == 'GET'

		year = request.GET.get('year', '')
		assert year.isnumeric()
		year = int(year)
		assert YEAR_BOUNDARIES[0] <= year <= YEAR_BOUNDARIES[1]

		months = range(1, 12 + 1)

		return JsonResponse({
			'categories': list(months),
			'series': [{
				'name': choice[1],
				'data': [len(Subscription.objects.filter(date__year=year, date__month=month, type=choice[0]))
				         for month in months]
			} for choice in SUBSCRIPTION_TYPE_CHOICES]})

	except AssertionError:
		return HttpResponseBadRequest()


@login_required
def get_renewals_for_year(request):
	years = range(YEAR_BOUNDARIES[0], YEAR_BOUNDARIES[1] + 1)

	return JsonResponse({
		'categories': list(years),
		'series': [{
			'name': RENEWED,
			'data': [sum(map(lambda sub: bool(sub) and bool(get(Subscription.objects.filter(customer=sub.customer,
			                                                                                date__year=year - 1), 0)),
			                 Subscription.objects.filter(date__year=year))) for year in years]
		}, {
			'name': NON_RENEWED,
			'data': [sum(map(lambda sub: bool(sub) and not bool(get(Subscription.objects.filter(customer=sub.customer,
			                                                                                    date__year=year - 1),
			                                                        0)),
			                 Subscription.objects.filter(date__year=year))) for year in years]
		}]})


@login_required
def get_earnings_per_year(request):
	if request.method == 'GET':
		year = request.GET.get('year', '')
		try:
			year = int(year)
			assert YEAR_BOUNDARIES[0] <= year <= YEAR_BOUNDARIES[1]
		except (ValueError, AssertionError):
			year = False

		if year:
			return JsonResponse({
				'labels': [choice[1] for choice in PROCESSING_TYPE_CHOICES],

				'datasets': [{
					'data': [sum(map(lambda x: x.price, Processing.objects.filter(date__year=year,
					                                                              type=choice[0])),
					             Decimal('0.00'))
					         for choice in PROCESSING_TYPE_CHOICES]
				}]
			})

		else:
			years = range(YEAR_BOUNDARIES[0], YEAR_BOUNDARIES[1] + 1)

			return JsonResponse({
				'categories': list(years),
				'series': [{
					'name': choice[1],
					'data': [sum(map(lambda x: x.price, Processing.objects.filter(date__year=year, type=choice[0])),
					             Decimal('0.00')) for year in years]
				} for choice in PROCESSING_TYPE_CHOICES]})
	else:
		return HttpResponseBadRequest()


def filter_queryset_in_years(queryset, from_, to):
	return {year: get(queryset.filter(date__year=year), 0) for year in range(from_, to + 1)}


def get(k, i, default=None):
	try:
		return k[i]
	except IndexError:
		return default
