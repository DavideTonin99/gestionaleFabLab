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
		context['subscriptions'] = {year: all_subs.filter(year__year=year) for year in range(2014, 2028 + 1)}
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
		initial['customer'] = self.get_customer()
		return initial

	def get_success_url(self):
		return reverse('gestionale_:update_subscription', args=(self.object.customer.id, self.object.id))

	def get_context_data(self, **kwargs):
		context = super(CreateSubscriptionView, self).get_context_data(**kwargs)
		context['op'] = 'Crea'

		customer = self.get_customer()
		context['id'] = customer.id

		all_subs = customer.subscription_set.all()
		context['show_tables'] = True
		context['subscriptions'] = {year: all_subs.filter(year__year=year) for year in range(2014, 2028 + 1)}

		return context
