from django.conf.urls import url

from .views import CreateCustomerView, UpdateCustomerView, CreateSubscriptionView, UpdateSubscriptionView, \
	CreateEventView, UpdateEventView, CreateProcessingView, UpdateProcessingView, get_participants_emails_csv, \
	get_homonyms, StatsView, get_associations_per_year, get_associations_per_month, get_renewals_for_year, \
	get_earnings_per_year

app_name = 'gestionale_'
urlpatterns = [
	url(r'^anagrafica/crea/$', CreateCustomerView.as_view(), name='create_customer'),
	url(r'^anagrafica/(?P<pk>[0-9]+)/$', UpdateCustomerView.as_view(), name='update_customer'),
	url(r'^anagrafica/iscrizioni/crea/(?P<customer_id>[0-9]+)/(?P<period>[0-9]{4}/[0-9]{4})/$',
	    CreateSubscriptionView.as_view(), name='create_subscription'),
	url(r'anagrafica/iscrizioni/(?P<pk>[0-9]+)/$', UpdateSubscriptionView.as_view(), name='update_subscription'),
	url(r'^eventi/crea/$', CreateEventView.as_view(), name='create_event'),
	url(r'^eventi/(?P<pk>[0-9]+)/$', UpdateEventView.as_view(), name='update_event'),
	url(r'^lavorazioni/crea/$', CreateProcessingView.as_view(), name='create_processing'),
	url(r'^lavorazioni/(?P<pk>[0-9]+)/$', UpdateProcessingView.as_view(), name='update_processing'),
	url(r'^statistiche/$', StatsView.as_view(), name='stats'),
	url(r'^ajax/customers/hm/$', get_homonyms, name='homonyms'),
	url(r'^ajax/events/pe/(?P<event_id>[0-9]+)/$', get_participants_emails_csv, name='participants_emails_csv'),
	url(r'^ajax/stats/ya/$', get_associations_per_year, name='associations_per_year'),
	url(r'^ajax/stats/ma/$', get_associations_per_month, name='associations_per_month'),
	url(r'^ajax/stats/yr/$', get_renewals_for_year, name='renewals_per_year'),
	url(r'^ajax/stats/ye/$', get_earnings_per_year, name='earnings_per_year')
]
