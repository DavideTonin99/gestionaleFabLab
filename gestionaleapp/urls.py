from django.conf.urls import url

from . import views

app_name = 'gestionale'
urlpatterns = [
    url(r'^anagrafica/$', views.CustomersView.as_view(), name="anagrafica"),
    url(r'^eventi/$', views.wip, name="eventi"),
    url(r'^lavorazioni/$', views.ProcessingsView.as_view(), name="lavorazioni"),
    url(r'^getclientdata/$', views.get_client_data, name="get_client_data"),
]
