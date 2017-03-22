from django.conf.urls import url

from . import views

app_name = 'gestionale'
urlpatterns = [
    url(r'^anagrafica/$', views.anagrafica),
    url(r'^eventi/$', views.eventi),
    url(r'^lavorazioni/$', views.lavorazioni),
]
