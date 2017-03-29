from django.conf.urls import url

from . import views

app_name = 'gestionale'
urlpatterns = [
    url(r'^anagrafica/$', views.customers, name="anagrafica"),
    url(r'^eventi/$', views.events, name="eventi"),
    url(r'^lavorazioni/$', views.processings, name="lavorazioni"),
    url(r'^getclientdata/$', views.get_client_data, name="get_client_data"),
    url(r'^handleclientdata/$', views.handle_client_data, name="handle_client_data")
]
