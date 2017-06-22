from datetime import date

from django.shortcuts import reverse, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView

from .models import Customer, Subscription
from .forms import CustomerForm, SubscriptionForm


class CreateCustomerView(LoginRequiredMixin, CreateView):
	model = Customer
	form_class = CustomerForm

	def get_success_url(self):
		return reverse('gestionale_:update_customer', args=(self.object.id,))

	def get_context_data(self, **kwargs):
		context = super(CreateCustomerView, self).get_context_data(**kwargs)
		context['customers'] = self.model.objects.all()
		context['op'] = 'Crea'
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
		context['customers'] = self.model.objects.all()
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

	def get_customer(self):
		return Customer.objects.filter(id=self.kwargs.get('customer_id')).get()

	def get_initial(self):
		initial = super(CreateSubscriptionView, self).get_initial()
		initial['customer'] = get_customer(self.kwargs.get('customer_id'))

		year = self.kwargs.get('year')
		if year:
			try:
				year = date(day=1, month=1, year=int(year))
				initial['year'] = year
			except ValueError:
				pass

		return initial

	def get_success_url(self):
		return reverse('gestionale_:update_subscription', args=(self.object.customer.id, self.object.id))

	def get_context_data(self, **kwargs):
		context = super(CreateSubscriptionView, self).get_context_data(**kwargs)
		context['op'] = 'Crea'

		customer = get_customer(self.kwargs.get('customer_id'))
		context['id'] = customer.id

		all_subs = customer.subscription_set.all()
		context['subscriptions'] = filter_queryset_in_years(all_subs, 2014, 2028)

		return context


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

		all_subs = self.object.customer.subscription_set.all()
		context['subscriptions'] = filter_queryset_in_years(all_subs, 2014, 2028)

		return context


def filter_queryset_in_years(queryset, from_, to):
	return {year: get(queryset.filter(year__year=year), 0) for year in range(from_, to + 1)}


def get_customer(id_):
	return get_object_or_404(Customer.objects.filter(id=id_))


def get(k, i, default=None):
	try:
		return k[i]
	except IndexError:
		return default
