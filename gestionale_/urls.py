from django.conf.urls import url

from .views import CreateCustomerView, UpdateCustomerView

app_name = 'gestionale_'
urlpatterns = [
	url(r'^anagrafica/crea/cliente$', CreateCustomerView.as_view(), name="create_customer"),
	url(r'^anagrafica/modifica/cliente/(?P<customer_id>[0-9]+)/$', UpdateCustomerView.as_view(), name="update_customer")
]
