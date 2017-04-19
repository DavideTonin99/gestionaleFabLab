from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'gestionale'
urlpatterns = [
    url(r'^anagrafica/$', login_required(views.CustomersView.as_view()), name="anagrafica"),
    url(r'^eventi/$', login_required(views.CustomersView.as_view()), name="eventi"),
    url(r'^lavorazioni/$', login_required(views.CustomersView.as_view()), name="lavorazioni"),
    url(r'^getclientdata/$', views.get_client_data, name="get_client_data"),
    url(r'^handleclientdata/$', views.handle_client_data, name="handle_client_data")
]
