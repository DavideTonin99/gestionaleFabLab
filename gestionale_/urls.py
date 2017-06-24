from django.conf.urls import url

from .views import CreateCustomerView, UpdateCustomerView, CreateSubscriptionView, UpdateSubscriptionView,\
	CreateEventView, UpdateEventView

app_name = 'gestionale_'
urlpatterns = [
	url(r'^anagrafica/crea/$', CreateCustomerView.as_view(), name='create_customer'),
	url(r'^anagrafica/modifica/(?P<customer_id>[0-9]+)/$', UpdateCustomerView.as_view(),
	    name='update_customer'),
	url(r'^anagrafica/(?P<customer_id>[0-9]+)/crea/(?:(?P<year>[0-9]{4})/)?$', CreateSubscriptionView.as_view(),
	    name='create_subscription'),
	url(r'anagrafica/(?P<customer_id>[0-9]+)/modifica/(?P<subscription_id>[0-9]+)/$', UpdateSubscriptionView.as_view(),
	    name='update_subscription'),
	url(r'^eventi/crea/$', CreateEventView.as_view(), name='create_event'),
	url(r'^eventi/modifica/(?P<event_id>[0-9]+)/$', UpdateEventView.as_view(), name='update_event')
]
