from django.shortcuts import reverse, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView

from .models import Customer
from .forms import CustomerForm


class CreateCustomerView(LoginRequiredMixin, CreateView):
    model = Customer
    form_class = CustomerForm

    def get_success_url(self):
        return reverse('gestionale_:create_customer')

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

        all_subs = self.object.subscription_set.all()
        context['subscriptions'] = {year: all_subs.filter(year__year=year) for year in range(2014, 2028 + 1)}

        context['processings'] = self.object.processing_set.all()
        return context
