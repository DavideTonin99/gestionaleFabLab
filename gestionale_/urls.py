from django.conf.urls import url

from .views import CreateCustomerView

app_name = 'gestionale_'
urlpatterns = [
    url(r'^anagrafica/crea/cliente$', CreateCustomerView.as_view(), name="create_customer"),
]
