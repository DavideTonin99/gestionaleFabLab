from django.conf.urls import url

from .views import CreateCustomerView, UpdateCustomerView, CreateSubscriptionView

app_name = 'gestionale_'
urlpatterns = [
	url(r'^anagrafica/crea/$', CreateCustomerView.as_view(), name='create_customer'),
	url(r'^anagrafica/modifica/(?P<customer_id>[0-9]+)/$', UpdateCustomerView.as_view(),
	    name='update_customer'),
	url(r'^anagrafica/(?P<customer_id>[0-9]+)/crea/(?:(?P<year>[0-9]{4})/)?$', CreateSubscriptionView.as_view(),
	    name='create_subscription'),
]
