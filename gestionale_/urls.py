from django.conf.urls import url

from .views import CreateCustomerView, UpdateCustomerView, CreateSubscriptionView, UpdateSubscriptionView, \
	CreateEventView, UpdateEventView, CreateProcessingView, UpdateProcessingView, get_participants_emails_csv,\
	get_homonyms, StatsView

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
	url(r'^eventi/modifica/(?P<event_id>[0-9]+)/$', UpdateEventView.as_view(), name='update_event'),
	url(r'^lavorazioni/crea/$', CreateProcessingView.as_view(), name='create_processing'),
	url(r'^lavorazioni/modifica/(?P<processing_id>[0-9]+)/$', UpdateProcessingView.as_view(), name='update_processing'),
	url(r'^gpec/(?P<event_id>[0-9]+)/$', get_participants_emails_csv, name='get_participants_emails_csv'),
	url(r'^gh/$', get_homonyms, name='get_homonyms'),
	url(r'^statistiche/$', StatsView.as_view(), name='stats')
]
